from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os

# ルーターのインポート
try:
    from app.routes import login, protected
    use_routes = True
except ImportError:
    use_routes = False

app = FastAPI()

# ルーターを追加（存在する場合のみ）
if use_routes:
    app.include_router(login.router)
    app.include_router(protected.router)

# 静的ファイル（CSS, JS）を提供
app.mount("/static", StaticFiles(directory="static"), name="static")

# ファイル保存用ディレクトリ
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 許可する拡張子
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".csv"}

@app.get("/")
def serve_login_page():
    return FileResponse("frontend/index.html")

@app.get("/admin_dashboard")
def serve_admin_dashboard():
    return FileResponse("frontend/admin_dashboard.html")

@app.get("/user_dashboard")
def serve_user_dashboard():
    return FileResponse("frontend/user_dashboard.html")

@app.get("/file_management")
def serve_file_management():
    return FileResponse("frontend/file_management.html")

@app.get("/point_management")
def serve_point_management():
    return FileResponse("frontend/point_management.html")

# 🔹 ファイルアップロード機能（許可された拡張子のみ受け入れ）
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # ファイル拡張子のチェック
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"この拡張子 ({file_ext}) は許可されていません")

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "アップロード成功", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"アップロードエラー: {str(e)}")

# 🔹 アップロード済みファイルの一覧を取得
@app.get("/files")
async def list_files():
    try:
        files = [{"name": f} for f in os.listdir(UPLOAD_DIR)]
        return JSONResponse(content=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイル取得エラー: {str(e)}")

# 🔹 ファイル削除機能（存在チェック & エラーハンドリング追加）
@app.delete("/delete")
async def delete_file(name: str):
    file_path = os.path.join(UPLOAD_DIR, name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="ファイルが見つかりません")

    try:
        os.remove(file_path)
        return {"message": f"{name} を削除しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"削除エラー: {str(e)}")
