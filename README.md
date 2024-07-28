### 零、VS code 操作
#### 1. Push

1. 到 Source Control
2. 在 Change 點選 + 號，將變動的部分移到 Staged Change
3. !!!! 針對你的變動部分，寫一段敘述在 Message !!!!
4. 點選右上角的 v，進行 commit
5. 點選 push，將修改的 commit push 到 remote repository

#### 2. Pull

1. 到 Source Control
2. 點選 ...，選擇 Pull







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





