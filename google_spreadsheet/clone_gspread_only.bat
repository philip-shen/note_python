git clone -n --depth=1 --filter=tree:0 https://github.com/philip-shen/note_python.git
cd note_python\
git sparse-checkout set --no-cone google_spreadsheet/gspread
git checkout