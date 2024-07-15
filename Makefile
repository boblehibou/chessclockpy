package: clean
	zip -r chessclockpy.zip chessclock

clean:
	-find chessclock -type d -name "__pycache__" -exec rm -rf {} \;

.PHONY: clean package
