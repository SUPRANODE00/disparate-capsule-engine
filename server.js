const express = require('express');
const cors = require('cors');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const app = express();
app.use(cors());
app.use(express.json());

const ajv = new Ajv({ allErrors: true, useDefaults: true });
addFormats(ajv);

// Schema 1: RF Physical Resource Telemetry Schema
const rfSchema = {
  type: 'object',
  properties: {
    resource_id: { type: 'string' },
    position_enu_m: {
      type: 'array',
      items: { type: 'number' },
      minItems: 3,
      maxItems: 3
    },
    rf: {
      type: 'object',
      properties: {
        mode: { type: 'string', enum: ['RX', 'TX', 'STANDBY', 'HOPPING'] },
        frequency_hz: { type: 'number' },
        bandwidth_hz: { type: 'number' },
        antenna_id: { type: 'string' },
        telemetry: {
          type: 'object',
          properties: {
            rssi_dbm: { type: 'number' },
            snr_db: { type: 'number' }
          },
          required: ['rssi_dbm', 'snr_db']
        }
      },
      required: ['mode', 'frequency_hz', 'bandwidth_hz', 'antenna_id', 'telemetry']
    }
  },
  required: ['resource_id', 'position_enu_m', 'rf']
};

// Schema 2: Initiate Allocation Payload Schema
const allocationSchema = {
  type: 'object',
  properties: {
    entity_id: { type: 'string', pattern: '^REG-\\d{4}-[A-Z]{2,4}-[a-f0-9]{8}$' },
    timestamp_utc: { type: 'string', format: 'date-time' },
    jurisdiction: { type: 'string' },
    administrative_status: { type: 'string', enum: ['PENDING', 'ACTIVE', 'SUSPENDED', 'DETACHED'] },
    origin_affinity: { type: 'string', default: 'TST_ORIGIN' }
  },
  required: ['entity_id', 'timestamp_utc', 'jurisdiction', 'administrative_status'],
  additionalProperties: false
};

const validateRF = ajv.compile(rfSchema);
const validateAllocation = ajv.compile(allocationSchema);

// Endpoint 1: RF Resource Ingest
app.post('/api/telemetry/rf', (req, res) => {
  const valid = validateRF(req.body);
  if (!valid) {
    return res.status(400).json({ status: 'ERROR', errors: validateRF.errors });
  }
  const { resource_id, position_enu_m, rf } = req.body;
  console.log(`[RF INGEST] Node: ${resource_id} | Mode: ${rf.mode} | Freq: ${(rf.frequency_hz / 1e6).toFixed(2)} MHz`);

  return res.status(200).json({
    status: 'ACK',
    timestamp_utc: new Date().toISOString(),
    node: resource_id,
    processed_position_enu: position_enu_m
  });
});

// Endpoint 2: Allocation Initiate
app.post('/api/allocation/initiate', (req, res) => {
  const valid = validateAllocation(req.body);
  if (!valid) {
    return res.status(400).json({ status: 'ERROR', errors: validateAllocation.errors });
  }

  console.log(`[ALLOCATION] Entity: ${req.body.entity_id} | Status: ${req.body.administrative_status}`);
  return res.status(201).json({
    status: 'ALLOCATED',
    entity_id: req.body.entity_id,
    origin_affinity: req.body.origin_affinity
  });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`===================================================`);
  console.log(` Telemetry & Allocation Daemon listening on :${PORT}`);
  console.log(` - POST /api/telemetry/rf`);
  console.log(` - POST /api/allocation/initiate`);
  console.log(`===================================================`);
});
