export function get(url, onsuccess = console.log, onerror = console.error) {
  fetch(url, { timeout: 3000 })
    .then((r) => r.json())
    .then(onsuccess)
    .catch(onerror);
}

export function post(url, data, onerror = console.error) {
  fetch(url, {
    timeout: 3000,
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).catch(onerror);
}
