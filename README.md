
pip install git+https://github.com/moolean/workTools.git

unzip background.zip

## 如何开发新种类chart

1. 使用规定的文件名(具体名字询问管理)：`chart_type`

2. 参考base_bar.py代码，修改chartdrawer函数内容，如默认生成的数据无法使用则修改datagenerater函数

        cp base_bar.py `chart_type`.py

`初始化类时一定要使用规定的type名称`
draw = bardrawer(chart_type = `chart_type`,  ...)

3. 生成图，生成100张图例

    python base_bar.py

生成图后会自动检查数据格式有无错误，打印以下信息说明无误

{'text_file': '', 'image_path': ''}
check image success.

4. 将浏览文件交给管理验收

    view_`chart_type`_time_usage.ipynb

5. 验收通过后上传git，一定要创建新分支在新分支上传

    git checkout -b [your_brancn_name] 
    git add `chart_type`.py
    git commit -m "`chart_type`"
    git push origin [your_brancn_name]
