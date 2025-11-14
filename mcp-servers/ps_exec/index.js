#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { 
  CallToolRequestSchema,
  ListToolsRequestSchema 
} from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const DISPATCHER_PATH = join(__dirname, 'dispatcher.ps1');

// Whitelist - No Invoke-Expression anywhere
const WHITELIST = {
  dir: { description: 'List directory contents' },
  type: { description: 'Read file contents' },
  test_path: { description: 'Test if path exists' },
  whoami: { description: 'Display current user' },
  get_process: { description: 'List running processes' },
  get_service: { description: 'List Windows services' },
  get_env: { description: 'Get environment variables' },
  test_connection: { description: 'Test network connectivity' },
  get_item_property: { description: 'Get registry or file properties' },
  measure_object: { description: 'Measure lines/words/chars in file' },
  screenshot: { description: 'Take a screenshot of the primary display' }
};

const server = new Server({
  name: 'ps_exec',
  version: '0.2.0'
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'ps_exec',
    description: 'Execute whitelisted PowerShell commands via secure dispatcher',
    inputSchema: {
      type: 'object',
      properties: {
        action: { 
          type: 'string', 
          enum: Object.keys(WHITELIST),
          description: 'Whitelisted action to perform'
        },
        args: { 
          type: 'object',
          description: 'Action-specific parameters',
          default: {}
        },
        timeoutSec: { 
          type: 'number', 
          default: 30,
          minimum: 1,
          maximum: 300
        }
      },
      required: ['action']
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { action, args = {}, timeoutSec = 30 } = request.params.arguments;
  
  if (!WHITELIST[action]) {
    throw new Error(`Action '${action}' not whitelisted`);
  }
  
  if (!existsSync(DISPATCHER_PATH)) {
    throw new Error(`Dispatcher not found: ${DISPATCHER_PATH}`);
  }
  
  return await execPS(action, args, timeoutSec);
});

async function execPS(action, args, timeoutSec) {
  return new Promise((resolve, reject) => {
    const argsJson = JSON.stringify(args);
    
    // Spawn PowerShell with -File (not -Command)
    const ps = spawn('powershell.exe', [
      '-NoProfile',
      '-NonInteractive',
      '-ExecutionPolicy', 'Bypass',
      '-File', DISPATCHER_PATH,
      '-Action', action,
      '-ArgsJson', argsJson
    ], {
      windowsHide: true,
      timeout: timeoutSec * 1000
    });
    
    let stdout = '';
    let stderr = '';
    let killed = false;
    
    ps.stdout.on('data', (data) => stdout += data.toString('utf8'));
    ps.stderr.on('data', (data) => stderr += data.toString('utf8'));
    
    // Timeout handler - kill process tree
    const timeout = setTimeout(() => {
      if (!killed) {
        killed = true;
        killProcessTree(ps.pid);
        reject(new Error(`Timeout after ${timeoutSec}s - process tree killed`));
      }
    }, timeoutSec * 1000);
    
    ps.on('error', (err) => {
      clearTimeout(timeout);
      reject(new Error(`Spawn error: ${err.message}`));
    });
    
    ps.on('close', (code) => {
      clearTimeout(timeout);
      
      if (killed) return;
      
      resolve({
        content: [{
          type: 'text',
          text: JSON.stringify({
            action: action,
            stdout: stdout.trim(),
            stderr: stderr.trim(),
            exitCode: code,
            timestamp: new Date().toISOString()
          }, null, 2)
        }]
      });
    });
  });
}

// Kill process tree using taskkill
function killProcessTree(pid) {
  try {
    spawn('taskkill', ['/PID', pid.toString(), '/T', '/F'], {
      windowsHide: true
    });
  } catch (err) {
    console.error(`Failed to kill process tree: ${err.message}`);
  }
}

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
console.error('ps_exec MCP server running');
