#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 查找最新版本的PlantUML jar
find_plantuml_jar() {
    local jar_path=$(find /usr/local/Cellar/plantuml -name "plantuml.jar" -type f | sort -r | head -n 1)
    if [ -z "$jar_path" ]; then
        echo -e "${RED}Error: PlantUML jar not found. Please ensure PlantUML is installed.${NC}"
        exit 1
    fi
    echo "$jar_path"
}

# 检查单个文件
check_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: File not found: $file${NC}"
        return 1
    fi

    echo -e "\n${GREEN}Checking $file...${NC}"
    echo "----------------------------------------"
    
    # 检查语法
    java -jar "$PLANTUML_JAR" -checkonly "$file" > /dev/null 2>&1
    syntax_status=$?
    
    if [ $syntax_status -eq 0 ]; then
        echo -e "${GREEN}✅ Syntax OK${NC}"
        
        # 尝试渲染
        java -jar "$PLANTUML_JAR" "$file" > /dev/null 2>&1
        render_status=$?
        
        if [ $render_status -eq 0 ]; then
            echo -e "${GREEN}✅ Render OK${NC}"
            # 检查是否生成了png文件
            png_file="${file%.*}.png"
            if [ -f "$png_file" ]; then
                echo -e "${GREEN}✅ Generated: $png_file${NC}"
            fi
            return 0
        else
            echo -e "${RED}❌ Render Failed${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Syntax Error${NC}"
        echo -e "\nFile contents with line numbers:"
        nl -ba "$file"
        return 1
    fi
}

# 显示使用方法
show_usage() {
    echo "Usage: $0 [file.puml]"
    echo "If no file is specified, checks all .puml files in the current directory and subdirectories"
    echo "Options:"
    echo "  -h, --help    Show this help message"
}

# 主函数
main() {
    # 查找PlantUML jar
    PLANTUML_JAR=$(find_plantuml_jar)
    echo -e "${YELLOW}Using PlantUML jar: $PLANTUML_JAR${NC}"

    # 处理命令行参数
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        show_usage
        exit 0
    fi

    # 如果指定了文件，只检查该文件
    if [ $# -eq 1 ]; then
        if [[ "$1" != *.puml ]]; then
            echo -e "${RED}Error: File must have .puml extension${NC}"
            exit 1
        fi
        check_file "$1"
        exit $?
    fi

    # 否则检查所有puml文件
    local error_found=0
    while IFS= read -r file; do
        check_file "$file"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error found in $file${NC}"
            error_found=1
            break
        fi
    done < <(find . -name "*.puml" -type f)

    if [ $error_found -eq 1 ]; then
        echo -e "${RED}Errors found. Stopping check.${NC}"
        exit 1
    else
        echo -e "${GREEN}All files checked successfully.${NC}"
        exit 0
    fi
}

# 运行主函数
main "$@" 