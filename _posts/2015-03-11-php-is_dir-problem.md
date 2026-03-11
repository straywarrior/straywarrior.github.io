---
layout: post
title: "PHP is_dir()函数出现的诡异问题"
date: 2015-03-11
categories: 
  - "linux"
---

系统环境：Cent OS 6.6

PHP版本：5.3.3

近日在Cent OS系统上搭建Cacti网管系统，Cacti版本0.8.8b，自带插件管理模块。准备安装monitor V1.3.1和weathermap V0.97c插件，将两个插件的压缩包下载至用户Downloads文件夹后，在当前文件夹内解压，并将解压后的插件文件夹monitor和weathermap通过root执行移动命令移入cacti的安装目录/var/www/cacti/plugins/，默认设置为归属root用户，权限755（Cacti目录亦归属root，权限777）。但是打开Cacti管理界面后无法从plugin management中找到插件。

排查PHP代码，从plugins.php中找到如下函数plugins\_load\_temp\_table()：

```
function plugins_load_temp_table() {
	global $config, $plugins;

	$pluginslist = retrieve_plugin_list();

	if (isset($_SESSION["plugin_temp_table"])) {
		$table = $_SESSION["plugin_temp_table"];
	}else{
		$table = "plugin_temp_table_" . rand();
	}
	$x = 0;
	while ($x < 30) {
		if (!plugins_temp_table_exists($table)) {
			$_SESSION["plugin_temp_table"] = $table;
			db_execute("CREATE TEMPORARY TABLE IF NOT EXISTS $table LIKE plugin_config");
			db_execute("TRUNCATE $table");
			db_execute("INSERT INTO $table SELECT * FROM plugin_config");
			break;
		}else{
			$table = "plugin_temp_table_" . rand();
		}
		$x++;
	}

	$path = $config['base_path'] . '/plugins/';
	$dh = opendir($path);
	if ($dh !== false) {
		while (($file = readdir($dh)) !== false) {
			if ((is_dir("$path/$file")) && (file_exists("$path/$file/setup.php")) && (!in_array($file, $pluginslist))) {
				include_once("$path/$file/setup.php");
				if (!function_exists('plugin_' . $file . '_install') && function_exists($file . '_version')) {
					$function = $file . '_version';
					$cinfo[$file] = $function();
					if (!isset($cinfo[$file]['author']))   $cinfo[$file]['author']   = 'Unknown';
					if (!isset($cinfo[$file]['homepage'])) $cinfo[$file]['homepage'] = 'Not Stated';
					if (isset($cinfo[$file]['webpage']))   $cinfo[$file]['homepage'] = $cinfo[$file]['webpage'];
					if (!isset($cinfo[$file]['longname'])) $cinfo[$file]['longname'] = ucfirst($file);
					$cinfo[$file]['status'] = -2;
					if (in_array($file, $plugins)) {
						$cinfo[$file]['status'] = -1;
					}
					db_execute("REPLACE INTO $table (directory, name, status, author, webpage, version)
						VALUES ('" .
							$file . "', '" .
							$cinfo[$file]['longname'] . "', '" .
							$cinfo[$file]['status']   . "', '" .
							$cinfo[$file]['author']   . "', '" .
							$cinfo[$file]['homepage'] . "', '" .
							$cinfo[$file]['version']  . "')");
					$pluginslist[] = $file;
				} elseif (function_exists('plugin_' . $file . '_install') && function_exists('plugin_' . $file . '_version')) {
					$function               = $file . '_version';
					$cinfo[$file]           = $function();
					$cinfo[$file]['status'] = 0;
					if (!isset($cinfo[$file]['author']))   $cinfo[$file]['author']   = 'Unknown';
					if (!isset($cinfo[$file]['homepage'])) $cinfo[$file]['homepage'] = 'Not Stated';
					if (isset($cinfo[$file]['webpage']))   $cinfo[$file]['homepage'] = $cinfo[$file]['webpage'];
					if (!isset($cinfo[$file]['longname'])) $cinfo[$file]['homepage'] = ucfirst($file);

					/* see if it's been installed as old, if so, remove from oldplugins array and session */
					$oldplugins = read_config_option("oldplugins");
					if (substr_count($oldplugins, $file)) {
						$oldplugins = str_replace($file, "", $oldplugins);
						$oldplugins = str_replace(",,", ",", $oldplugins);
						$oldplugins = trim($oldplugins, ",");
						set_config_option('oldplugins', $oldplugins);
						$_SESSION['sess_config_array']['oldplugins'] = $oldplugins;
					}

					db_execute("REPLACE INTO $table (directory, name, status, author, webpage, version)
						VALUES ('" .
							$file . "', '" .
							$cinfo[$file]['longname'] . "', '" .
							$cinfo[$file]['status'] . "', '" .
							$cinfo[$file]['author'] . "', '" .
							$cinfo[$file]['homepage'] . "', '" .
							$cinfo[$file]['version'] . "')");
					$pluginslist[] = $file;
				}
			}
		}
		closedir($dh);
	}

	return $table;
}
```

该函数在plugins.php加载时被调用，调用栈为update\_show\_current()->plugins\_load\_temp\_table()

其中is\_dir()函数经测试后证明对plugins/下所有路径全部返回false，在其它目录下手动编写一个测试脚本test.php测试is\_dir()后也返回false。但在plugins/目录下用root用户新建一个目录test/之后，对该路径is\_dir()返回true。因此尝试删除原来的monitor和weathermap文件夹，将压缩包复制如plugins/用root用户执行解压，所得目录的用户和权限均完全相同，is\_dir()果然返回正确。

其原因目前尚不得知，有待探查。
