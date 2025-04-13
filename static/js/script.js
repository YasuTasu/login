// ログイン処理
async function login(role) {
    const userIdInput = document.getElementById(role + "_user_id");
    const passwordInput = document.getElementById(role + "_password");
    const errorMessage = document.getElementById(role + "-error-message");

    const userIdRaw = userIdInput.value;
    const userId = userIdRaw.trim().toLowerCase();
    const password = passwordInput.value.trim();

    console.log("🔍 [生ID] 入力されたユーザーID:", userIdRaw);
    console.log("🧼 [整形後] 小文字＆trimしたユーザーID:", userId);

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userIdRaw, password: password, role: role })
    });

    const data = await response.json();
    console.log("✅ レスポンス:", data);

    if (response.ok) {
        console.log("🚀 ログイン成功！分岐処理へ");
        console.log("🎯 最終分岐判定: userId === 'test_user' ? →", userId === "test_user");

        if (userId === "test_user") {
            window.location.href = "https://v0-happy-point-program-howr15.vercel.app/dashboard";
        } else if (userId === "admin_user") {
            alert("✅ admin_user に一致。外部URLへリダイレクトします。");
            window.location.href = "https://v0-happy-point-program-howr15.vercel.app/admin";
        } else {
            alert("✅ その他ユーザー。ローカル画面にリダイレクトします。");
            window.location.href = role === "admin" ? "/admin_dashboard" : "/user_dashboard";
        }
    } else {
        errorMessage.textContent = data.detail || "ログインに失敗しました";
    }
}


// ファイルアップロード処理
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("ファイルを選択してください。");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        alert("アップロード成功");
        loadFiles();
    } else {
        alert("アップロード失敗");
    }
}

// ファイル一覧をロード（ダミーデータ + API 取得データを併存）
async function loadFiles() {
    const response = await fetch("/files");
    const files = await response.json();

    const tableBody = document.getElementById("fileTableBody");

    // 既存のダミーデータを維持しながら、新しいデータを追加
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
// 選択したファイルを表示
function selectFile(fileName) {
    document.getElementById("selected-file").textContent = `選択中のファイル: ${fileName}`;
    localStorage.setItem("selectedFile", fileName);
}

// ファイル編集処理（仮実装）
function editFile() {
    const fileName = localStorage.getItem("selectedFile");
    if (!fileName) {
        alert("ファイルを選択してください。");
        return;
    }
    alert(`ファイル「${fileName}」の編集画面を開きます（未実装）`);
}

// ファイル提出処理（仮実装）
function submitFile() {
    const fileName = localStorage.getItem("selectedFile");
    if (!fileName) {
        alert("ファイルを選択してください。");
        return;
    }
    alert(`ファイル「${fileName}」を提出しました`);
}

// ファイル削除処理
async function deleteFile() {
    const fileName = localStorage.getItem("selectedFile");
    if (!fileName) {
        alert("ファイルを選択してください。");
        return;
    }

    const response = await fetch(`/delete?name=${fileName}`, {
        method: "DELETE"
    });

    if (response.ok) {
        alert(`ファイル「${fileName}」を削除しました`);
        loadFiles();
        document.getElementById("selected-file").textContent = "選択中のファイル: なし";
        localStorage.removeItem("selectedFile");
    } else {
        alert("削除に失敗しました");
    }
}

// ページ遷移
function navigateTo(path) {
    window.location.href = path;
}

// ログアウト処理
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    window.location.href = "/";
}

// ページロード時にファイル一覧を読み込む
window.onload = function() {
    if (window.location.pathname === "/file_management") {
        loadFiles();
    }
};
