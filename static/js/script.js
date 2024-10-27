const API_BASE_URL = '/dev';  // Define the base URL path

// Create Item
document.getElementById('createForm').onsubmit = async function (e) {
    e.preventDefault();
    const item_id = document.getElementById('createItemId').value;
    const name = document.getElementById('createName').value;
    const response = await fetch(`${API_BASE_URL}/items`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id, name })
    });
    alert('Item Created');
};

// Get Item
document.getElementById('getForm').onsubmit = async function (e) {
    e.preventDefault();
    const item_id = document.getElementById('getItemId').value;
    const response = await fetch(`${API_BASE_URL}/items/${item_id}`);
    const data = await response.json();
    document.getElementById('getResult').innerText = JSON.stringify(data, null, 2);
};

// Update Item
document.getElementById('updateForm').onsubmit = async function (e) {
    e.preventDefault();
    const item_id = document.getElementById('updateItemId').value;
    const name = document.getElementById('updateName').value;
    const response = await fetch(`${API_BASE_URL}/items/${item_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    alert('Item Updated');
};

// Delete Item
document.getElementById('deleteForm').onsubmit = async function (e) {
    e.preventDefault();
    const item_id = document.getElementById('deleteItemId').value;
    await fetch(`${API_BASE_URL}/items/${item_id}`, { method: 'DELETE' });
    alert('Item Deleted');
};

// List All Items
document.getElementById('listButton').onclick = async function () {
    const response = await fetch(`${API_BASE_URL}/items`);
    const data = await response.json();
    document.getElementById('listResult').innerText = JSON.stringify(data, null, 2);
};