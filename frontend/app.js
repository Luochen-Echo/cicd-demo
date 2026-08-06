export async function fetchHealth() {
  const res = await fetch('/api/health')
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export function formatHealth(data) {
  return `状态:${data.status} 数据库:${data.db ? '已连接' : '未连接'}`
}

if (typeof document !== 'undefined') {
  const refreshBtn = document.getElementById('refresh')
  const output = document.getElementById('output')

  refreshBtn.addEventListener('click', async () => {
    try {
      const data = await fetchHealth()
      output.textContent = formatHealth(data)
    } catch (err) {
      output.textContent = `请求失败: ${err.message}`
    }
  })
}
