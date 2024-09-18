
import os, sys, shutil
import subprocess
import win32file
import argparse
from windows_metadata import WindowsAttributes

# You can assign path of your toolchain here manually.
path_toolchain_beplnex_src_mono_x86 = None # Download beplnex5 for mono from https://github.com/BepInEx/BepInEx/releases
path_toolchain_beplnex_src_mono_x64 = None
path_toolchain_beplnex_src_il2cpp_x86 = None # Download beplnex6 for il2cpp from https://builds.bepinex.dev/projects/bepinex_be
path_toolchain_beplnex_src_il2cpp_x64 = None
path_toolchain_cpp2il = None # Download cpp2il from https://github.com/SamboyCoding/Cpp2IL/releases
path_toolchain_il2cpp_dumper = None # (Optional) Download il2cpp_dumper from https://github.com/Perfare/Il2CppDumper/releases
path_toolchain_il2cpp_unhollower = None # (Optional) Download il2cpp_unhollower from https://github.com/knah/Il2CppAssemblyUnhollower/releases
path_toolchain_unity_explorer_mono = None
path_toolchain_unity_explorer_il2cpp = None

def string_has_tail(string, tail):
	return (len(string) >= len(tail)) and string[-len(tail):] == tail

def determine_file_arch(path_file):
	if os.path.isfile(path_file):
		arch_file = win32file.GetBinaryType(path_file)
		if arch_file == win32file.SCS_32BIT_BINARY:
			return 86
		if arch_file == 6: # win32file does not offer constant SCS_64BIT_BINARY so I hardcoded here. Of course it should not support, since it's name is "win32file" !!!
			return 64
	return None

def determine_path_toolchain(path_dir_self):
	global path_toolchain_beplnex_src_mono_x86
	global path_toolchain_beplnex_src_mono_x64
	global path_toolchain_beplnex_src_il2cpp_x86
	global path_toolchain_beplnex_src_il2cpp_x64
	global path_toolchain_cpp2il
	global path_toolchain_il2cpp_dumper
	global path_toolchain_il2cpp_unhollower
	global path_toolchain_unity_explorer_mono
	global path_toolchain_unity_explorer_il2cpp

	path_dir_toolchain = os.path.join(path_dir_self, "toolchain")
	if os.path.isdir(path_dir_toolchain):
		for name_item in os.listdir(path_dir_toolchain):
			path_item = os.path.join(path_dir_toolchain, name_item)

			# Determine beplnex source by winhttp.dll.
			path_file_winhttp = os.path.join(path_item, "winhttp.dll")
			if os.path.isdir(os.path.join(path_item, "BepInEx", "core")) and os.path.isfile(path_file_winhttp):

				# determine_file_arch only works for .exe files, but there is no .exe file in beplnex source. Have to find arch by name here ...
				arch = None
				if "x86" in name_item.lower():
					arch = 86
				if "x64" in name_item.lower():
					arch = 64

				if os.path.isdir(os.path.join(path_item, "dotnet")): # il2cpp
					if (arch == 86) and (path_toolchain_beplnex_src_il2cpp_x86 is None):
						path_toolchain_beplnex_src_il2cpp_x86 = path_item
					if (arch == 64) and (path_toolchain_beplnex_src_il2cpp_x64 is None):
						path_toolchain_beplnex_src_il2cpp_x64 = path_item
				else: # Mono
					if (arch == 86) and (path_toolchain_beplnex_src_mono_x86 is None):
						path_toolchain_beplnex_src_mono_x86 = path_item
					if (arch == 64) and (path_toolchain_beplnex_src_mono_x64 is None):
						path_toolchain_beplnex_src_mono_x64 = path_item

			# Determine path_toolchain_cpp2il by name.
			if ("cpp2il" in name_item.lower()) and string_has_tail(name_item.lower(), ".exe") and (path_toolchain_cpp2il is None):
				path_toolchain_cpp2il = path_item

			# Determine path_toolchain_il2cpp_dumper.
			path_il2cpp_dumper = os.path.join(path_item, "Il2CppDumper.exe")
			if os.path.isfile(path_il2cpp_dumper) and (path_toolchain_il2cpp_dumper is None):
				path_toolchain_il2cpp_dumper = path_il2cpp_dumper

			# Determine path_toolchain_il2cpp_unhollower.
			path_il2cpp_unhollower = os.path.join(path_item, "AssemblyUnhollower.exe")
			if os.path.isfile(path_il2cpp_unhollower) and (path_toolchain_il2cpp_unhollower is None):
				path_toolchain_il2cpp_unhollower = path_il2cpp_unhollower

			# Determine Unity Explorer.
			path_toolchain_unity_explorer = os.path.join(path_item, "plugins", "sinai-dev-UnityExplorer")
			if os.path.isfile(os.path.join(path_toolchain_unity_explorer, "UnityExplorer.BIE5.Mono.dll")):
				path_toolchain_unity_explorer_mono = path_toolchain_unity_explorer
			if os.path.isfile(os.path.join(path_toolchain_unity_explorer, "UnityExplorer.BIE.IL2CPP.dll")):
				path_toolchain_unity_explorer_il2cpp = path_toolchain_unity_explorer

	if path_toolchain_beplnex_src_mono_x86 is None:
		print("Warning: path_toolchain_beplnex_src_mono_x86 not found.")
	if path_toolchain_beplnex_src_mono_x64 is None:
		print("Warning: path_toolchain_beplnex_src_mono_x64 not found.")
	if path_toolchain_beplnex_src_il2cpp_x86 is None:
		print("Warning: path_toolchain_beplnex_src_il2cpp_x86 not found.")
	if path_toolchain_beplnex_src_il2cpp_x64 is None:
		print("Warning: path_toolchain_beplnex_src_il2cpp_x64 not found.")
	if path_toolchain_cpp2il is None:
		print("Warning: path_toolchain_cpp2il not found.")
	if path_toolchain_il2cpp_dumper is None:
		print("Warning: path_toolchain_il2cpp_dumper not found.")
	if path_toolchain_il2cpp_unhollower is None:
		print("Warning: path_toolchain_il2cpp_unhollower not found.")
	if path_toolchain_unity_explorer_mono is None:
		print("Warning: path_toolchain_unity_explorer_mono not found.")
	if path_toolchain_unity_explorer_il2cpp is None:
		print("Warning: path_toolchain_unity_explorer_il2cpp not found.")

determine_path_toolchain(os.path.dirname(os.path.abspath(__file__)))

def string_sub_tail(string, tail):
	if string_has_tail(string, tail):
		return string[:-len(tail)]
	else:
		return string

def ensure_dir(path_dir):
	if not os.path.isdir(path_dir):
		os.makedirs(path_dir)

def copy_dir(path_src, path_dst):
	if os.path.isdir(path_src):
		ensure_dir(path_dst)
	for name_item in os.listdir(path_src):
		path_item_src = os.path.join(path_src, name_item)
		path_item_dst = os.path.join(path_dst, name_item)
		if os.path.isfile(path_item_src):
			if not os.path.isfile(path_item_dst): # non-replace copy.
				shutil.copyfile(path_item_src, path_item_dst)
		if os.path.isdir(path_item_src):
			copy_dir(path_item_src, path_item_dst)

def fetch_mono_tfm(path_dir_game_data_mono):
	path_file_dll_netstandard = os.path.join(path_dir_game_data_mono, "netstandard.dll")
	if os.path.isfile(path_file_dll_netstandard):
		metainfo = WindowsAttributes(path_file_dll_netstandard)
		metainfo_version = metainfo["File version"]
		netstandard_version = '.'.join(metainfo_version.split('.')[:2])
		return "netstandard" + netstandard_version

	path_file_dll_mscorlib = os.path.join(path_dir_game_data_mono, "mscorlib.dll")
	if os.path.isfile(path_file_dll_mscorlib):
		metainfo = WindowsAttributes(path_file_dll_mscorlib)
		metainfo_version = metainfo["File version"]
		metainfo_version_major = int(metainfo_version.split('.')[0])
		netframework_version = "46" if metainfo_version_major >= 4 else "35"
		return "net" + netframework_version

	return None

def fetch_mono_unity(path_file_exe_unity):
	if os.path.isfile(path_file_exe_unity):
		metainfo = WindowsAttributes(path_file_exe_unity)
		metainfo_version = metainfo["File version"]
		unity_version = '.'.join(metainfo_version.split('.')[:3])
		return unity_version
	return None

def run_process(text_command, path_working=None):
	print("Running: {}".format(text_command))
	p = None
	if path_working is None:
		p = subprocess.Popen(text_command)
	else:
		p = subprocess.Popen(text_command, cwd=path_working)
	p.wait()
	streamdata = p.communicate()[0]
	code = p.returncode
	print("return code: {}".format(code))
	return code == 0

def check_list_path_lib_assembly(path_dir_game_data_mono, list_name_lib_assembly, list_path_lib_assembly):
	if list_name_lib_assembly is None:
		list_name_lib_assembly = []
	list_name_lib_assembly = list_name_lib_assembly + ["Assembly-CSharp.dll", "UnityEngine.UI.dll", "UnityEngine.CoreModule.dll", "Il2Cppmscorlib.dll", "UnhollowerBaseLib.dll"]

	if list_path_lib_assembly is None:
		list_path_lib_assembly = []

	for name_lib_assembly in list_name_lib_assembly:
		list_path_lib_assembly.append(os.path.join(path_dir_game_data_mono, name_lib_assembly))

	return list(filter(os.path.isfile, list_path_lib_assembly))

def list_single(item):
	if isinstance(item, list) and (len(item) == 1):
		return item[0]
	return item

def process(args):
	path_dir_game = args.path_dir_game
	name_project = args.name_project
	path_dir_game_projects = os.path.join(path_dir_game, "BepInEx_Projects")

	list_name_dir_game_data = []
	for name_dir in os.listdir(path_dir_game):
		if string_has_tail(name_dir, "_Data"):
			list_name_dir_game_data.append(name_dir)
	if len(list_name_dir_game_data) != 1:
		print("Cannot determine game data folder!")
		return False
	name_dir_game_data = list_name_dir_game_data[0]
	path_dir_game_data = os.path.join(path_dir_game, name_dir_game_data)

	path_file_exe_unity = list_single(args.path_file_exe_unity)
	if path_file_exe_unity is None:
		name_file_exe_unity = list_single(args.name_file_exe_unity)
		if name_file_exe_unity is None:
			name_file_exe_unity = string_sub_tail(name_dir_game_data, "_Data") + ".exe"
		path_file_exe_unity = os.path.join(path_dir_game, name_file_exe_unity)
		if not os.path.isfile(path_file_exe_unity):
			list_name_file = os.listdir(path_dir_game)
			list_name_file = list(filter(lambda name_file: string_has_tail(name_file, ".exe") and (name_file != "UnityCrashHandler64.exe"), list_name_file))
			list_path_file = list(map(lambda name_file: os.path.join(path_dir_game, name_file)))
			if len(list_path_file) == 1:
				path_file_exe_unity = list_single(list_path_file)
	if not os.path.isfile(path_file_exe_unity):
		print("Cannot determine game exe file:")
		print("    {}".format(path_file_exe_unity))
		print("is not a file.")
		return False

	# Fetch assembly architecture.
	beplnex_info_arch = determine_file_arch(path_file_exe_unity)
	if beplnex_info_arch is None:
		print("Cannot determine unity architecture (x86 or x64).")
		return False
	print("Arch: x{}".format(beplnex_info_arch))

	# Determine unity is mono or il2cpp.
	path_toolchain_beplnex_src = None
	path_dir_assembly_source = None
	path_toolchain_unity_explorer = None
	path_dir_game_data_mono = os.path.join(path_dir_game_data, "Managed")
	path_dir_game_data_il2cpp = os.path.join(path_dir_game_data, "il2cpp_data")

	if os.path.isdir(path_dir_game_data_mono):
		print("Unity pack version: mono")

		# Determine beplnex version.
		if beplnex_info_arch == 86:
			path_toolchain_beplnex_src = path_toolchain_beplnex_src_mono_x86
		if beplnex_info_arch == 64:
			path_toolchain_beplnex_src = path_toolchain_beplnex_src_mono_x64
		if (path_toolchain_beplnex_src is None) or (not os.path.isdir(os.path.join(path_toolchain_beplnex_src, "BepInEx"))):
			print("Cannot find toolchain: beplnex.")
			return False

		# Copy corresponding beplnex files.
		copy_dir(path_toolchain_beplnex_src, path_dir_game)

		# Fetch game info where beplnex requires.
		beplnex_info_tfm = fetch_mono_tfm(path_dir_game_data_mono)
		if beplnex_info_tfm is None:
			print("Cannot determine beplnex TFM")
			return False
		print("TFM: {}".format(beplnex_info_tfm))

		beplnex_info_unity = fetch_mono_unity(path_file_exe_unity)
		if beplnex_info_unity is None:
			print("Cannot determine beplnex unity")
			return False
		print("Unity: {}".format(beplnex_info_unity))

		# Run command to create beplnex project.
		ensure_dir(path_dir_game_projects)
		if not run_process("dotnet new bepinex5plugin -n {} -T {} -U {}".format(name_project, beplnex_info_tfm, beplnex_info_unity), path_dir_game_projects):
			print("Failed to create beplnex project")
			return False

		# Assign assembly source directory for project processing.
		path_dir_assembly_source:str = path_dir_game_data_mono

		# Assign path of unity explorer.
		if not args.skip_explorer:
			path_toolchain_unity_explorer = path_toolchain_unity_explorer_mono

	if os.path.isdir(path_dir_game_data_il2cpp):
		print("Unity pack version: IL2CPP")
		path_file_gameassembly = os.path.join(path_dir_game, "GameAssembly.dll")

		# Determine beplnex version.
		if beplnex_info_arch == 86:
			path_toolchain_beplnex_src = path_toolchain_beplnex_src_il2cpp_x86
		if beplnex_info_arch == 64:
			path_toolchain_beplnex_src = path_toolchain_beplnex_src_il2cpp_x64
		if (path_toolchain_beplnex_src is None) or (not os.path.isdir(os.path.join(path_toolchain_beplnex_src, "BepInEx"))):
			print("Cannot find toolchain: beplnex.")
			return False

		# Process step1.
		il2cpp_use_dumper:bool = args.il2cpp_use_dumper
		path_dir_game_data_il2cpp_step1:str = None
		command_il2cpp_step1:str = None

		if il2cpp_use_dumper:
			# Make sure that il2cpp_dumper is valid.
			if (path_toolchain_il2cpp_dumper is None) or (not os.path.isfile(path_toolchain_il2cpp_dumper)):
				print("Cannot find toolchain: il2cpp_dumper.")
				return False
			
			# Generate command for il2cpp_dumper.
			path_dir_game_data_il2cpp_step1 = path_dir_game_data + "_il2cppdumper"
			command_il2cpp_step1 = "\"{}\" \"{}\" \"{}\" \"{}\"".format(
				path_toolchain_il2cpp_dumper,
				path_file_gameassembly,
				os.path.join(path_dir_game_data_il2cpp, "Metadata", "global-metadata.dat"),
				path_dir_game_data_il2cpp_step1,
			)
		else:
			# Make sure that cpp2il is valid.
			if (path_toolchain_cpp2il is None) or (not os.path.isfile(path_toolchain_cpp2il)):
				print("Cannot find toolchain: cpp2il.")
				return False
			
			# Generate command for cpp2il.
			path_dir_game_data_il2cpp_step1 = path_dir_game_data + "_cpp2il"
			command_il2cpp_step1 = "{} --game-path \"{}\" --exe-name \"{}\" --output-root \"{}\"".format(path_toolchain_cpp2il, path_dir_game, string_sub_tail(os.path.basename(path_file_exe_unity), ".exe"), path_dir_game_data_il2cpp_step1)
			if not args.il2cpp_skip_step2:
				command_il2cpp_step1 = "{} --skip-analysis --skip-metadata-txts --disable-registration-prompts".format(command_il2cpp_step1) # https://github.com/BepInEx/Il2CppInterop/blob/master/Documentation/Command-Line-Usage.md
		
		ensure_dir(path_dir_game_data_il2cpp_step1)
		if not run_process(command_il2cpp_step1):
			if il2cpp_use_dumper:
				print("Failed to run il2cpp_dumper.")
			else:
				print("Failed to run cpp2il.")
			return False
		else:
			if il2cpp_use_dumper:
				path_dir_game_data_il2cpp_step1 = os.path.join(path_dir_game_data_il2cpp_step1, "DummyDll")
		path_dir_assembly_source = path_dir_game_data_il2cpp_step1

		# Process step2.
		if not args.il2cpp_skip_step2:
			il2cpp_use_unhollower:bool = args.il2cpp_use_unhollower
			path_dir_game_data_il2cpp_step2:str = None
			command_il2cpp_step2:str = None
			if il2cpp_use_unhollower:
				# Make sure that il2cpp_unhollower is valid.
				if (path_toolchain_il2cpp_unhollower is None) or (not os.path.isfile(path_toolchain_il2cpp_unhollower)):
					print("Cannot find toolchain: il2cpp_unhollower.")
					return False
				
				# Generate command for il2cpp_unhollower.
				path_dir_game_data_il2cpp_step2 = path_dir_game_data + "_unhollowed"
				path_file_dll_mscorlib = os.path.join(path_dir_game_data_il2cpp_step1, "mscorlib.dll") # From step 1.
				# path_file_dll_mscorlib = os.path.join(path_dir_game, "dotnet", "mscorlib.dll") # From beplnex IL2CPP. This does not work, why???
				command_il2cpp_step2 = "\"{}\" --input=\"{}\" --output=\"{}\" --mscorlib=\"{}\"".format(
					path_toolchain_il2cpp_unhollower,
					path_dir_game_data_il2cpp_step1,
					path_dir_game_data_il2cpp_step2,
					path_file_dll_mscorlib,
				)
			else:
				# Generate command for il2cpp_interop.
				path_dir_game_data_il2cpp_step2 = path_dir_game_data + "_interop"
				ensure_dir(path_dir_game_data_il2cpp_step2)
				command_il2cpp_step2 = "il2cppinterop generate --input \"{}\" --output \"{}\" --game-assembly \"{}\"".format(path_dir_game_data_il2cpp_step1, path_dir_game_data_il2cpp_step2, path_file_gameassembly)
			if not run_process(command_il2cpp_step2):
				if il2cpp_use_unhollower:
					print("Failed to run il2cpp_unhollower")
				else:
					print("Failed to run il2cpp interop")
				return False
			path_dir_assembly_source = path_dir_game_data_il2cpp_step2

		# Copy corresponding beplnex files.
		copy_dir(path_toolchain_beplnex_src, path_dir_game)

		# Run command to create beplnex project.
		ensure_dir(path_dir_game_projects)
		if not run_process("dotnet new bep6plugin_unity_il2cpp -n {}".format(name_project), path_dir_game_projects):
			print("Failed to create beplnex project")
			return False

		# Assign path of unity explorer.
		if not args.skip_explorer:
			path_toolchain_unity_explorer = path_toolchain_unity_explorer_il2cpp

	# project processing.
	if not (path_dir_assembly_source is None):

		# Restore beplnex project.
		path_dir_game_project = os.path.join(path_dir_game_projects, name_project)
		path_file_game_project = os.path.join(path_dir_game_project, name_project + ".csproj")
		if not run_process("dotnet restore \"{}\"".format(path_file_game_project)):
			print("Failed to restore beplnex project")
			return False

		# copy lib files.
		list_path_lib_assembly = check_list_path_lib_assembly(path_dir_assembly_source, args.list_name_lib_assembly, args.list_path_lib_assembly)
		path_dir_game_project_lib = os.path.join(path_dir_game_project, "lib")
		ensure_dir(path_dir_game_project_lib)
		for path_lib_assembly in list_path_lib_assembly:
			path_file_src = path_lib_assembly
			path_file_dst = os.path.join(path_dir_game_project_lib, os.path.basename(path_lib_assembly))
			if not os.path.isfile(path_file_dst):
				shutil.copyfile(path_file_src, path_file_dst)

		# Modify .csproj files.
		print("Modify {} ...".format(path_file_game_project))
		file_game_project = open(path_file_game_project, "r")
		lines = file_game_project.readlines()
		file_game_project.close()

		line_prefix = None
		line_num_insert = None
		line_feed = "\n"
		for line_num in range(len(lines) - 1, 0, -1):
			if line_num_insert is None:
				line = lines[line_num]
				line_prefix_len = line.find("</ItemGroup>")
				if line_prefix_len >= 0:
					line_num_insert = line_num
					line_prefix = line[:line_prefix_len]
					if '\r' in line:
						line_feed = "\r\n"
		if line_num_insert is None:
			print("Cannot find line in csproj to insert content.")
			return False
		line_num_insert = line_num_insert + 1

		lines_insert = []
		lines_insert.append(line_prefix)
		lines_insert.append(line_prefix + "<ItemGroup>")
		for path_lib_assembly in list_path_lib_assembly:
			name_lib_assembly = os.path.basename(path_lib_assembly)
			lines_insert.append(line_prefix + line_prefix + "<Reference Include=\"{}\">".format(name_lib_assembly))
			lines_insert.append(line_prefix + line_prefix + line_prefix + "<HintPath>lib\\{}</HintPath>".format(name_lib_assembly))
			lines_insert.append(line_prefix + line_prefix + "</Reference>")
		lines_insert.append(line_prefix + "</ItemGroup>")
		lines_insert.append(line_prefix)
		lines_insert.append(line_prefix + "<Target Name=\"CopyCustomContent\" AfterTargets=\"AfterBuild\">")
		lines_insert.append(line_prefix + line_prefix + "<Copy SourceFiles=\"$(OutDir)\\$(AssemblyName).dll\" DestinationFolder=\"..\\..\\BepInEx\\plugins\" />")
		lines_insert.append(line_prefix + "</Target>")

		for line_num in range(len(lines_insert)):
			lines_insert[line_num] = lines_insert[line_num] + line_feed

		lines = lines[:line_num_insert] + lines_insert + lines[line_num_insert:]

		file_game_project = open(path_file_game_project, "w")
		file_game_project.writelines(lines)
		file_game_project.close()

		# Copy unity explorer.
		if not path_toolchain_unity_explorer is None:
			print("Deploy unity explorer ...")
			copy_dir(path_toolchain_unity_explorer, os.path.join(path_dir_game, "BepInEx", "plugins", "sinai-dev-UnityExplorer"))

		print("\nDone.")
		return True
	else:
		print("Unity pack version is not mono. Currently not supported.")
		return False

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Autodeploy beplnex projects.')
	parser.add_argument('path_dir_game', metavar='PATH_DIR_GAME', help='Path of your game directory. Usually contains your game exe file and a XXX_Data folder.')
	parser.add_argument('name_project', metavar='NAME_PROJECT', help="Name of your dotnet project.")
	parser.add_argument('-nfeu', '--name_file_exe_unity', nargs=1, metavar='NAME_FILE_EXE_UNITY', help="When name of exe file is not PATH_DIR_GAME.exe, you have to specify it manually.")
	parser.add_argument('-pfeu', '--path_file_exe_unity', nargs=1, metavar='PATH_FILE_EXE_UNITY', help="When path of exe is not PATH_DIR_GAME\\PATH_DIR_GAME.exe, you have to specify it manually.")
	parser.add_argument('-lnla', '--list_name_lib_assembly', nargs='+', metavar=('NAME_LIB_ASSEMBLY_1', 'NAME_LIB_ASSEMBLY_2'), help="List of libs names you wish to depend on besides Assembly-CSharp.dll.")
	parser.add_argument('-lpla', '--list_path_lib_assembly', nargs='+', metavar=('PATH_LIB_ASSEMBLY_1', 'PATH_LIB_ASSEMBLY_2'), help="List of libs paths you wish to depend on besides Assembly-CSharp.dll.")
	parser.add_argument('-ics2', '--il2cpp_skip_step2', help="Skip Il2Cpp interop or unhollower.", action='store_true')
	parser.add_argument('-se', '--skip_explorer', help="Do not deploy unity explorer, a plugin for convenience.", action='store_true')
	parser.add_argument('-icud', '--il2cpp_use_dumper', help="Use il2cppdumper instead of cpp2il.", action='store_true')
	parser.add_argument('-icuu', '--il2cpp_use_unhollower', help="Use il2cppunhollower instead of il2cppinterop.", action='store_true')
	args = parser.parse_args()

	process(args)
