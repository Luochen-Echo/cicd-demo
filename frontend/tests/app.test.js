import test from 'node:test'
import assert from 'node:assert/strict'

import { formatHealth } from '../app.js'

test('formatHealth 输出后端状态和数据库连接情况', () => {
  assert.equal(formatHealth({ status: 'ok', db: true }), '状态:ok 数据库:已连接')
  assert.equal(formatHealth({ status: 'ok', db: false }), '状态:ok 数据库:未连接')
})
