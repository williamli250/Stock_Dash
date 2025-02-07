### 一、VS code 操作
#### 1-1. Push

1. 到 Source Control
2. 在 Change 點選 + 號，將變動的部分移到 Staged Change
3. **!!!! 針對你的變動部分，寫一段敘述在 Message !!!!**
4. 點選右上角的 v，進行 commit
5. 點選 push，將修改的 commit push 到 remote repository
6. 完成


#### 1-2. Pull

1. 到 Source Control
2. 點選 ...，選擇 Pull
3. 完成


### 二、終端機操作

cd Desktop/Stock_Dash/code

python index.py


### 三、如何跟 Github Repository 連線

1. 將資料上傳到 Github Repository
2. 打開 VS code，開啟檔案的部分選擇「從 Github Clone 到本機端」（給它 URL，選擇好本機端目的地）
3. 完成


### 四、Git 分支合併操作

- 方法 1：使用 git reset (修改歷史)（這會覆寫遠端倉庫的歷史）
	1.	強制回到指定的 commit
        - git reset --hard yyyyyyyeeeeeeeeeeeeee
	2.	強制推送到遠端
        - git push --force
- 方法 2：使用 git revert (保留歷史)
    1.	回滾到指定的 commit
        - git revert --no-commit HEAD~1
    2.	提交回滾
        - git commit -m "Revert to commit yyyyyyyeeeeeeeeeeeeee"
	3.	推送到遠端
        - git push
- 方法 3：建立新分支來回朔
	1.	建立新分支並回到指定 commit
        - git checkout -b rollback-branch yyyyyyyeeeeeeeeeeeeee
    2. 	推送新分支
        - git push -u origin rollback-branch
    3.	如果確定要回到該版本，可以合併回主分支
        - git checkout main
        - git merge rollback-branch
        - git push




