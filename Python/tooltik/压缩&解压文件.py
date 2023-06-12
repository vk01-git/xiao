import zipfile

# 打开ZIP文件
with zipfile.ZipFile('example.zip', 'r') as zip_ref:
    # 解压所有文件到当前目录
    zip_ref.extractall('.')


import zipfile

# 创建ZIP文件并设置密码
with zipfile.ZipFile('example.zip', 'w', zipfile.ZIP_DEFLATED) as zip_ref:
    zip_ref.setpassword(b'mypassword') # 设置密码
    # 将文件夹添加到ZIP文件中
    zip_ref.write('myfolder', compress_type=zipfile.ZIP_DEFLATED)


import bpy

# 创建一个立方体
bpy.ops.mesh.primitive_cube_add(size=2)

# 将立方体移动到指定位置
bpy.context.object.location = (0, 0, 0)

# 渲染场景
bpy.ops.render.render(write_still=True)
