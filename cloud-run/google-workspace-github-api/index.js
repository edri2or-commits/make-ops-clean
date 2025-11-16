const express = require('express');
const axios = require('axios');
const { google } = require('googleapis');

const app = express();
app.use(express.json());

// Health check
app.get('/', (req, res) => {
  res.json({ service: 'google-workspace-github-api', status: 'ok' });
});

// Simple helper to log without crashing
function log(...args) {
  try {
    console.log(...args);
  } catch (e) {}
}

/**
 * POST /github/update-file
 * Body: { repo, branch, path, content, message }
 *
 * Uses GITHBUB_TOKEN (env) to call GitHub REST API.
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
      'User-Agent': 'google-workspace-github-api',
      Accept: 'application/vund.github+json',
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
      `${ apiBase }/repos/${repo}/contents/${encodeURIComponent(path)}`,
      {
        message,
        content: Buffer.from(content, "utf8").toString('base64'),
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
  log(`google-workspace-github-api listening on port ${port}`);
});