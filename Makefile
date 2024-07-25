# SPDX-FileCopyrightText: 2024 Boris Stefanovic <owldev@bluewin.ch>
#
# SPDX-License-Identifier: GPL-3.0-only

PROJNAME := chessclockpy
NAME := chessclock

MAIN := launch.py
MAKEFILE := Makefile
LICENCE := LICENCE.txt
NOTICE := NOTICE.txt

PYTHON ?= python
VENV := venv
REQS := requirements.txt

OUT := out

ZIP_DIR_NAME := ${PROJNAME}
ZIP_DIR_PATH := ${OUT}/${ZIP_DIR_NAME}
ZIP_FILE := ${PROJNAME}.zip
ZIP_PATH := ${OUT}/${ZIP_FILE}

BIN_ROOT := ${OUT}/inst
BIN_SPEC := ${BIN_ROOT}
BIN_WORK := ${BIN_ROOT}/build
BIN_DIST := ${OUT}



all: package bin

run: ${VENV}
	source ${VENV}/bin/activate && \
		${PYTHON} ${MAIN} && \
		deactivate

package: ${OUT}
	rm -rf ${ZIP_DIR_PATH} ${ZIP_PATH}
	mkdir -p ${ZIP_DIR_PATH}
	cp -r chessclock ${MAIN} ${REQS} ${MAKEFILE} ${LICENCE} ${NOTICE} ${ZIP_DIR_PATH}/
	cd ${OUT} && \
		zip -r ${ZIP_FILE} ${ZIP_DIR_NAME}

bin: ${OUT} ${VENV}
	rm -rf ${BIN_ROOT}
	mkdir -p ${BIN_ROOT}
	source ${VENV}/bin/activate && \
		pip install -U pyinstaller && \
		pyinstaller \
			-y \
			--clean \
			--onefile \
			--windowed \
			--distpath ${BIN_DIST} \
			--workpath ${BIN_WORK} \
			--specpath ${BIN_SPEC} \
			--name ${NAME} \
			launch.py && \
		deactivate

run-bin: bin
	./out/${NAME}

clean:
	-find chessclock -type d -name "__pycache__" -exec rm -rf {} \;
	rm -rf ${OUT} build dist *.spec
	rm -rf ${VENV}

${VENV}:
	-[[ ! -d ${VENV} ]] && \
		${PYTHON} -m venv ${VENV} && \
		source ${VENV}/bin/activate && \
		pip install -U pip && \
		pip install -U -r ${REQS} && \
		deactivate

${OUT}:
	mkdir -p $@



.PHONY: all bin clean package run run-bin
