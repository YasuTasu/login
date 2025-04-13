async function loadFiles() {
    const response = await fetch("/files");
    const files = await response.json();

    const tableBody = document.getElementById("fileTableBody");

    files.forEach(file => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>API</td>
            <td>${file.name}</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
            <td><button onclick="selectFile('${file.name}')">選択</button></td>
        `;
        tableBody.appendChild(row);
    });
}

function selectFile(fileId) {
    document.getElementById("selected-file").textContent = `選択中のファイル: ${fileId}`;
    localStorage.setItem("selectedFile", fileId);
}

function editFile() {
    alert("編集機能（仮実装）");
}

function submitFile() {
    alert("提出機能（仮実装）");
}

function deleteFile() {
    alert("削除機能（仮実装）");
}

function navigateTo(path) {
    window.location.href = path;
}

window.onload = function() {
    if (window.location.pathname === "/file_management") {
        loadFiles();
    }
};

