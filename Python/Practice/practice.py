# # #1.输出和变量
# # print("hello")

# # name = "rock_01"
# # count = 5
# # scale = 1.5
# # is_valid = True

# # print(name)
# # print(count + 10)
# # print(is_valid)


# # #2.字符串
# # name = "SM_rock_01.fbx"

# # print(len(name)) #returns the number of items (length) in an object
# # print(name.upper()) #returns name in upper case only
# # print(name.lower()) #returns name in lower case only
# # print(name.replace("rock", "wall")) #replace the word rock with wall
# # print(name.split(".")) #split the name into 2 word before and after the dot
# # print(name.startswith("SM_")) #print all name starts with xx
# # print(name.endswith(".fbx")) #print all name ends with xx
# # print(name.strip()) #remove white space

# # count = 3
# # print(f"found {count} assets named{name}")



# #3.列表
# # assets = ["rocks", "wall", "floor"]

# # # print(assets[0])
# # # print(assets[-1])
# # # print(len(assets))

# # # assets.append("ceiling")
# # # assets.remove("wall")
# # # print(assets)

# # print(sorted(assets))
# # print("rock" in assets)


# #4.循环
# # for a in assets:
# #     print(a)

# # for i in range(5):
# #     print(i)

# # for i, a in enumerate(assets):
# #     print(i,a)


# # #5.条件
# # count = 7

# # if count > 10:
# #     print("too many")
# # if count < 5:
# #     print("ok")
# # else:
# #     print("too few")

# # if count > 5 and count < 10:
# #     print("in range")

# # if not "rock" in assets:
# #     print("missing")


# #6.字典
# #You define a dictionary using curly braces {} with colons separating keys and values

# # asset = {
# #     "name": "rock_01",
# #     "tris": 4200,
# #     "material": "M_rock",
# # }

# # # print(asset["name"])
# # # print(asset.get("lod", 0))

# # asset["tris"] = 3800
# # asset["lod"] = 2

# # for key in asset:
# #     print(key, asset[key])

# # for key, value in asset.items():
# #     print(key,value)


# # #7.函数
# # def check_tris(count):
# #     if count > 5000:
# #         return False
# #     return True

# # print(check_tris(4200))
# # print(check_tris(9000))

# # def rename(name, prefix = "SM_"):
# #     return prefix + name

# # print(rename("rock_01"))
# # print(rename("rock_01","SK_"))


# #8.路径和文件
# import os

# folder = "C:/assets"
# #Path Management
# print(os.path.exists(folder))
# print(os.path.join(folder, "rock.fbx"))
# print(os.path.basename("C:/assets/rock.fbx"))
# print(os.path.splitext("rock.fbx"))

# #Lists only the items sitting directly inside C:/assets. It does not look inside any subfolders.
# for f in os.listdir(folder):
#     print(f)

# #A powerful scanner that goes down through every subfolder automatically.
# for root,dirs,files in os.walk(folder):
#     for f in files:
#         print(os.path.join(root,f))


# with open("report.txt", "w") as f:
#     f.write("line one\n")
#     f.write("line two\n")

# with open("report.txt", "r") as f:
#     content = f.read()
#     print(content)


# #9.异常

# try:
#     value = int("abc")
# except ValueError as e:
#     print(f"failed: {e}")

# failed = []

# for a in assets:
#     try:
#         process(a)
#     except Exception as e:
#         failed.append((a, str(e)))

# print(f"done. {len(failed)} failed.")

import os
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))
XLSX_PATH = os.path.join(PROJECT_ROOT, "docs", "module_list.xlsx")
OUT_PATH = os.path.join(HERE, "output", "module_list.csv")
SHEET_NAME = "Module List"

print(SHEET_NAME)