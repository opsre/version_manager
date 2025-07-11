#!/bin/bash

# 配置参数
API_BASE_URL="http://192.168.0.11:5000/api/v1"
PRODUCT_CODE="meituan"  # 替换为实际的产品code
VERSION_NUMBER="1.0.0"  # 替换为要查询的版本号

# 函数：一次性获取版本锁定状态（优化版）
get_version_lock_status_optimized() {
    local product_code=$1
    local version_number=$2
    
    echo "正在查询产品code: $product_code, 版本号: $version_number 的锁定状态..."
    
    # 获取所有产品列表
    products_response=$(curl -s "$API_BASE_URL/products?per_page=1000")
    
    # 检查API调用是否成功
    if [ $? -ne 0 ]; then
        echo "错误：获取产品列表失败"
        return 1
    fi
    
    # 查找指定code的产品ID
    product_id=$(echo "$products_response" | jq -r ".data.products[] | select(.code == \"$product_code\") | .id")
    
    if [ "$product_id" = "null" ] || [ -z "$product_id" ]; then
        echo "未找到产品code为 $product_code 的产品"
        return 1
    fi
    
    #echo "找到产品ID: $product_id"
    
    # 获取该产品的所有版本
    versions_response=$(curl -s "$API_BASE_URL/versions?product_id=$product_id")
    
    # 检查API调用是否成功
    if [ $? -ne 0 ]; then
        echo "错误：获取版本列表失败"
        return 1
    fi
    
    # 查找指定版本号的锁定状态
    lock_status=$(echo "$versions_response" | jq -r ".data.versions[] | select(.version_number == \"$version_number\") | .lock_status")
    
    if [ "$lock_status" = "null" ] || [ -z "$lock_status" ]; then
        echo "未找到版本号为 $version_number 的版本"
        return 1
    elif [ "$lock_status" = "true" ]; then
        echo "产品 $product_code 的版本 $version_number 已锁定"
        return 0
    else
        echo "产品 $product_code 的版本 $version_number 未锁定"
        return 0
    fi
}

# 调用函数
get_version_lock_status_optimized "$PRODUCT_CODE" "$VERSION_NUMBER"
