#!/usr/bin/env node
const https = require("https");
const fs = require("fs");
const path = require("path");

const envPath = path.resolve(__dirname, "..", ".env");
const env = Object.fromEntries(
  fs.readFileSync(envPath, "utf8")
    .split(/\r?\n/)
    .filter(l => l && !l.startsWith("#") && l.includes("="))
    .map(l => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim()]; })
);

const TOKEN = env.MAKE_API_KEY;
const ZONE = env.MAKE_ZONE || "eu2";
const SCENARIO_ID = env.MAKE_SCENARIO_ID;
const HOOK_ID = 4094313;
const GMAIL_CONN = 14146466;
const SHEETS_CONN = 14146482;
const SPREADSHEET_ID = env.GOOGLE_SPREADSHEET_ID;
const NOTIFY_TO = "mdzainulabidin11@gmail.com";

function api(method, p, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const req = https.request({
      hostname: `${ZONE}.make.com`,
      path: p,
      method,
      headers: {
        "Authorization": `Token ${TOKEN}`,
        "Content-Type": "application/json",
        ...(data ? { "Content-Length": Buffer.byteLength(data) } : {})
      }
    }, res => {
      let buf = "";
      res.on("data", c => (buf += c));
      res.on("end", () => {
        const out = { status: res.statusCode, body: buf };
        try { out.json = JSON.parse(buf); } catch {}
        resolve(out);
      });
    });
    req.on("error", reject);
    if (data) req.write(data);
    req.end();
  });
}

const blueprint = {
  name: "Vapi Call Report Processor",
  flow: [
    {
      id: 1,
      module: "gateway:CustomWebHook",
      version: 1,
      parameters: { hook: HOOK_ID, maxResults: 1 },
      mapper: {},
      metadata: {
        designer: { x: 0, y: 0 },
        restore: { parameters: { hook: { label: "Vapi Call Report", data: { editable: "true" } } } },
        parameters: [
          { name: "hook", type: "hook:gateway-webhook", label: "Webhook", required: true },
          { name: "maxResults", type: "number", label: "Maximum number of results" }
        ],
        interface: [{ name: "message", type: "collection", spec: [] }],
        advanced: true
      }
    },
    {
      id: 2,
      module: "google-email:sendAnEmail",
      version: 4,
      parameters: { __IMTCONN__: GMAIL_CONN },
      filter: {
        name: "Only end-of-call-report",
        conditions: [[
          { a: "{{1.message.type}}", b: "end-of-call-report", o: "text:equal" }
        ]]
      },
      mapper: {
        to: [NOTIFY_TO],
        cc: [],
        bcc: [],
        subject: "PolarCrest Call — {{ifempty(1.message.call.customer.number; \"Unknown caller\")}}",
        contentType: "html",
        html: [
          "<h2 style=\"font-family:sans-serif\">PolarCrest Call Report</h2>",
          "<table style=\"font-family:sans-serif;border-collapse:collapse\">",
          "<tr><td><b>Caller</b></td><td>{{1.message.call.customer.number}}</td></tr>",
          "<tr><td><b>Duration</b></td><td>{{floor(1.message.durationSeconds / 60)}}m {{round(1.message.durationSeconds % 60)}}s</td></tr>",
          "<tr><td><b>Cost</b></td><td>${{formatNumber(1.message.cost; 4; \".\"; \"\")}}</td></tr>",
          "<tr><td><b>Ended</b></td><td>{{1.message.endedReason}}</td></tr>",
          "</table>",
          "<h3>Summary</h3><p>{{1.message.summary}}</p>",
          "<h3>Recording</h3><p><a href=\"{{1.message.recordingUrl}}\">Listen to call</a></p>",
          "<h3>Transcript</h3><pre style=\"font-family:monospace;white-space:pre-wrap\">{{1.message.transcript}}</pre>"
        ].join(""),
        attachments: []
      },
      metadata: {
        designer: { x: 300, y: 0 },
        restore: { parameters: { __IMTCONN__: { label: "My Gmail connection (zsdigitalmovies139@gmail.com)", data: { scoped: "true", connection: "google-email" } } } },
        parameters: [
          { name: "__IMTCONN__", type: "account:google-email", label: "Connection", required: true }
        ],
        expect: [
          { name: "to", type: "array", label: "To", required: true, spec: { type: "email" } },
          { name: "cc", type: "array", label: "Copy recipient", spec: { type: "email" } },
          { name: "bcc", type: "array", label: "Blind copy recipient", spec: { type: "email" } },
          { name: "subject", type: "text", label: "Subject" },
          { name: "contentType", type: "select", label: "Content Type", validate: { enum: ["html", "text"] } },
          { name: "html", type: "text", label: "Content" },
          { name: "attachments", type: "array", label: "Attachments" }
        ]
      }
    },
    {
      id: 3,
      module: "google-sheets:addRow",
      version: 2,
      parameters: { __IMTCONN__: SHEETS_CONN },
      mapper: {
        from: "drive",
        mode: "select",
        spreadsheetId: `/${SPREADSHEET_ID}`,
        sheetId: "Calls",
        includesHeaders: true,
        insertUnformatted: false,
        insertDataOption: "INSERT_ROWS",
        valueInputOption: "USER_ENTERED",
        values: {
          "0": "{{formatDate(now; \"YYYY-MM-DD HH:mm\"; \"America/Toronto\")}}",
          "1": "{{1.message.call.customer.number}}",
          "2": "{{floor(1.message.durationSeconds / 60)}}:{{if(length(toString(1.message.durationSeconds % 60)) = 1; \"0\" + toString(1.message.durationSeconds % 60); toString(1.message.durationSeconds % 60))}}",
          "3": "{{formatNumber(1.message.cost; 4; \".\"; \"\")}}",
          "4": "{{1.message.endedReason}}",
          "5": "{{1.message.summary}}",
          "6": "{{1.message.recordingUrl}}"
        }
      },
      metadata: {
        designer: { x: 600, y: 0 },
        restore: {
          parameters: {
            __IMTCONN__: { label: "My Google connection (mdzainulabidin11@gmail.com)", data: { scoped: "true", connection: "google" } },
            from: { label: "Select from the List" },
            mode: { label: "Select" },
            sheetId: { label: "Calls" }
          }
        },
        parameters: [
          { name: "__IMTCONN__", type: "account:google", label: "Connection", required: true }
        ],
        expect: [
          { name: "from", type: "select", label: "Choose a Method", required: true, validate: { enum: ["drive", "url"] } },
          { name: "mode", type: "select", label: "Mode", required: true, validate: { enum: ["select", "fromAll", "map"] } },
          { name: "spreadsheetId", type: "file", label: "Spreadsheet ID", required: true },
          { name: "sheetId", type: "text", label: "Sheet Name", required: true },
          { name: "includesHeaders", type: "boolean", label: "Table contains headers" },
          { name: "insertUnformatted", type: "boolean", label: "Insert as unformatted" },
          { name: "insertDataOption", type: "select", label: "Insert data option", validate: { enum: ["INSERT_ROWS", "OVERWRITE"] } },
          { name: "valueInputOption", type: "select", label: "Value input option", validate: { enum: ["USER_ENTERED", "RAW"] } },
          { name: "values", type: "collection", label: "Values" }
        ]
      }
    }
  ],
  metadata: {
    instant: true,
    version: 1,
    scenario: {
      roundtrips: 1,
      maxErrors: 10,
      autoCommit: true,
      autoCommitTriggerLast: true,
      sequential: false,
      slots: null,
      confidential: false,
      dataloss: false,
      dlq: false,
      freshVariables: false
    },
    designer: { orphans: [] },
    zone: `${ZONE}.make.com`,
    notes: []
  }
};

(async () => {
  console.log(`Patching scenario ${SCENARIO_ID}...`);

  // Step 1: Push the fixed blueprint
  const patch = await api("PATCH", `/api/v2/scenarios/${SCENARIO_ID}?confirmed=true`, {
    blueprint: JSON.stringify(blueprint),
    scheduling: JSON.stringify({ type: "indefinitely", interval: 900 })
  });
  console.log("Blueprint PATCH →", patch.status);
  if (patch.json?.scenario) {
    console.log("  isinvalid:", patch.json.scenario.isinvalid);
    console.log("  isActive :", patch.json.scenario.isActive);
  } else {
    console.log(patch.body.slice(0, 500));
    process.exit(1);
  }

  if (patch.json.scenario.isinvalid) {
    console.error("Blueprint still invalid — check Make UI for details.");
    process.exit(1);
  }

  // Step 2: Activate
  const activate = await api("PATCH", `/api/v2/scenarios/${SCENARIO_ID}`, {
    isActive: true
  });
  console.log("Activate PATCH →", activate.status);
  console.log("  isActive:", activate.json?.scenario?.isActive);

  console.log("\nDone. Scenario is live and valid.");
})();
