### 一、終端機操作

cd Desktop/Stock_DSS/code

python index.py

### 二、Github Push
1. 提交本地變更

cd Desktop/Stock_DSS/code

git add .

git commit -m "Save local changes"

2. 拉取遠端變更（Pull）

git pull origin main --rebase

3. 解決衝突（如果有）

git add <file>
git rebase --continue

4. 推送本地變更（Push）

git push -u origin main

### 三、Github Pull

1. 取消本地變更 和 清理未追踪的文件

git reset --hard

git clean -fd

2. 拉取遠端代碼

git pull origin main





