const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

// Health check with capabilities
app.get('/', (req, res) => {
  res.json({
    service: 'github-executor-api',
    version: '1.0.0',
    status: 'ok',
    capabilities: ['read-file', 'update-doc']
  });
});

// Simple helper to log without crashing
function log(...args) {
  try {
    console.log(...args);
  } catch (e) {}
}

/**
 * Path validation for OS_SAFE operations
 * Returns true if path is in allowed safe scope
 */
function isPathSafe(path) {
  if (!path || typeof path !== 'string') {
    return false;
  }

  // Check for directory traversal attempts
  if (path.includes('../') || path.includes('..\\')) {
    return false;
  }

  // Allowed path prefixes (OS_SAFE)
  const safePrefixes = [
    'DOCS/',
    'logs/',
    'OPS/STATUS/',
    'OPS/EVIDENCE/'
  ];

  // Check if path starts with any safe prefix
  if (safePrefixes.some(prefix => path.startsWith(prefix))) {
    return true;
  }

  // Allowed patterns (STATE_FOR_GPT files)
  if (/^STATE_FOR_GPT.*\.md$/.test(path)) {
    return true;
  }

  return false;
}

/**
 * GET /repo/read-file
 * Read a single file from GitHub repository
 * 
 * Body: { owner, repo, path, ref? }
 */
app.post('/repo/read-file', async (req, res) => {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    return res.status(500).json({ error: 'GITHUB_TOKEN not configured' });
  }

  const { owner, repo, path, ref } = req.body || {};
  if (!owner || !repo || !path) {
    return res.status(400).json({
      error: 'missing_required_fields',
      required: ['owner', 'repo', 'path']
    });
  }

  // Validate path for safety
  if (path.includes('../') || path.includes('..\\')) {
    return res.status(400).json({
      error: 'invalid_path',
      details: 'Path contains directory traversal attempt'
    });
  }

  try {
    const apiBase = 'https://api.github.com';
    const headers = {
      Authorization: `token ${token}`,
      'User-Agent': 'github-executor-api',
      Accept: 'application/vnd.github+json',  // FIXED: was 'vund'
    };

    const refParam = ref ? `?ref=${ref}` : '';
    const getResp = await axios.get(
      `${apiBase}/repos/${owner}/${repo}/contents/${encodeURIComponent(path)}${refParam}`,
      { headers }
    );

    if (!getResp.data) {
      return res.status(404).json({
        error: 'file_not_found',
        details: `File does not exist at path: ${path}`
      });
    }

    // Decode content if base64
    let content = getResp.data.content;
    if (getResp.data.encoding === 'base64') {
      content = Buffer.from(content, 'base64').toString('utf-8');
    }

    return res.json({
      status: 'ok',
      content: content,
      path: getResp.data.path,
      sha: getResp.data.sha,
      encoding: 'utf-8'
    });
  } catch (err) {
    log('Error in /repo/read-file:', err.response?.status, err.response?.data || err.message);
    
    if (err.response?.status === 404) {
      return res.status(404).json({
        error: 'file_not_found',
        details: `File does not exist at path: ${path}`
      });
    }

    return res.status(500).json({
      error: 'github_read_failed',
      details: err.response?.data || err.message,
    });
  }
});

/**
 * POST /repo/update-doc
 * Create or update a file in OS_SAFE paths only
 * 
 * Body: { owner, repo, path, content, commit_message, branch? }
 */
app.post('/repo/update-doc', async (req, res) => {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    return res.status(500).json({ error: 'GITHUB_TOKEN not configured' });
  }

  const { owner, repo, path, content, commit_message, branch } = req.body || {};
  if (!owner || !repo || !path || !content || !commit_message) {
    return res.status(400).json({
      error: 'missing_required_fields',
      required: ['owner', 'repo', 'path', 'content', 'commit_message']
    });
  }

  // CRITICAL: Path validation for OS_SAFE operations only
  if (!isPathSafe(path)) {
    return res.status(403).json({
      error: 'OUT_OF_SAFE_SCOPE',
      details: `Path '${path}' is not in allowed safe paths`,
      allowed_paths: [
        'DOCS/',
        'logs/',
        'OPS/STATUS/',
        'OPS/EVIDENCE/',
        'STATE_FOR_GPT*.md'
      ]
    });
  }

  try {
    const apiBase = 'https://api.github.com';
    const headers = {
      Authorization: `token ${token}`,
      'User-Agent': 'github-executor-api',
      Accept: 'application/vnd.github+json',  // FIXED: was 'vund'
    };

    const branchParam = branch || 'main';

    // Get file SHA if exists (for update)
    let sha = undefined;
    try {
      const getResp = await axios.get(
        `${apiBase}/repos/${owner}/${repo}/contents/${encodeURIComponent(path)}?ref=${branchParam}`,
        { headers }
      );
      if (getResp && getResp.data && getResp.data.sha) {
        sha = getResp.data.sha;
      }
    } catch (e) {
      // File doesn't exist - this is fine, we'll create it
      if (e.response && e.response.status !== 404) {
        throw e;
      }
    }

    // Create or update file
    const putResp = await axios.put(
      `${apiBase}/repos/${owner}/${repo}/contents/${encodeURIComponent(path)}`,
      {
        message: commit_message,
        content: Buffer.from(content, 'utf8').toString('base64'),
        branch: branchParam,
        sha,
      },
      { headers }
    );

    return res.json({
      status: 'ok',
      action: sha ? 'update' : 'create',
      commit_sha: putResp.data.commit.sha,
      content: {
        path: putResp.data.content.path,
        sha: putResp.data.content.sha,
      },
    });
  } catch (err) {
    log('Error in /repo/update-doc:', err.response?.status, err.response?.data || err.message);
    return res.status(500).json({
      error: 'github_update_failed',
      details: err.response?.data || err.message,
    });
  }
});

/**
 * LEGACY ENDPOINT: /github/update-file
 * Kept for backward compatibility, but redirects to /repo/update-doc logic
 * @deprecated Use /repo/update-doc instead
 */
app.post('/github/update-file', async (req, res) => {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    return res.status(500).json({ error: 'GITHUB_TOKEN not configured' });
  }

  const { repo, branch, path, content, message } = req.body || {};
  if (!repo || !branch || !path || !content || !message) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  try {
    const apiBase = 'https://api.github.com';
    const headers = {
      Authorization: `token ${token}`,
      'User-Agent': 'github-executor-api',
      Accept: 'application/vnd.github+json',  // FIXED: was 'vund'
    };

    // Get file SHA if exists
    let sha = undefined;
    try {
      const getResp = await axios.get(
        `${apiBase}/repos/${repo}/contents/${encodeURIComponent(path)}?ref=${branch}`,
        { headers }
      );
      if (getResp && getResp.data && getResp.data.sha) {
        sha = getResp.data.sha;
      }
    } catch (e) {
      if (e.response && e.response.status !== 404) {
        throw e;
      }
    }

    const putResp = await axios.put(
      `${apiBase}/repos/${repo}/contents/${encodeURIComponent(path)}`,
      {
        message,
        content: Buffer.from(content, 'utf8').toString('base64'),
        branch,
        sha,
      },
      { headers }
    );

    return res.json({
      status: 'ok',
      action: sha ? 'update' : 'create',
      commit_sha: putResp.data.commit.sha,
      content: {
        path: putResp.data.content.path,
        sha: putResp.data.content.sha,
      },
    });
  } catch (err) {
    log('Error in /github/update-file:', err.response?.status, err.response?.data || err.message);
    return res.status(500).json({
      error: 'github_update_failed',
      details: err.response?.data || err.message,
    });
  }
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  log(`github-executor-api v1.0.0 listening on port ${port}`);
});
