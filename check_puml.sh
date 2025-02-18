#!/bin/zsh

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Find PlantUML jar
PLANTUML_JAR=$(find /usr/local/Cellar/plantuml -name plantuml.jar | sort -r | head -n 1)
echo "Using PlantUML jar: $PLANTUML_JAR"

# Check a single file
check_file() {
    local file="$1"
    echo "\nChecking $file..."
    echo "----------------------------------------"
    
    if [ ! -f "$file" ]; then
        echo "❌ File not found: $file"
        return 1
    fi
    
    # Check syntax
    java -jar "$PLANTUML_JAR" -checkonly "$file"
    if [ $? -eq 0 ]; then
        echo "✅ Syntax OK"
        
        # Try to render
        java -jar "$PLANTUML_JAR" "$file"
        if [ $? -eq 0 ]; then
            echo "✅ Render OK"
            return 0
        else
            echo "❌ Render Failed"
            return 1
        fi
    else
        echo "❌ Syntax Error"
        echo "\nFile contents with line numbers:"
        nl -ba "$file"
        return 1
    fi
}

# 显示使用方法
show_help() {
    echo "Usage: $0 [file1.puml file2.puml ...]"
    echo "Checks PlantUML files for syntax and rendering."
    echo ""
    echo "If no files are specified, checks all .puml files in current directory."
}

# 主函数
main() {
    # 处理命令行参数
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_help
        exit 0
    fi

    # If no arguments provided, check all .puml files
    if [[ $# -eq 0 ]]; then
        echo "No file specified. Checking all .puml files...\n"
        for file in *.puml; do
            check_file $file
        done
    else
        # Check each specified file
        for file in "$@"; do
            check_file $file
        done
    fi
}

# 运行主函数
main "$@" 