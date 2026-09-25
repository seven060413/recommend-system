function loadRecommend() {
    // 1. 获取当前用户
    let username = sessionStorage.getItem('currentUser') || '张三';

    // 2. 发起后端请求
    fetch(`http://127.0.0.1:5000/recommend/${username}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP 错误: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log("后端返回:", data);

            // ==========================================
            // 3. 显示相似用户 (顶部)
            // ==========================================
            const usersDiv = document.getElementById("users");
            if (usersDiv) {
                if (data.similar_users && data.similar_users.length > 0) {
                    usersDiv.innerHTML = data.similar_users.map(user => `
                        <div class="card" style="flex: 1; min-width: 200px; text-align: center; padding: 16px; margin-bottom: 0;">
                            <h3 style="margin-bottom: 8px; font-size: 16px; color: #333;">👤 ${user.user}</h3>
                            <p style="font-size: 13px; color: #666; margin-bottom: 4px;">
                                相似度: <span style="color: #ff5000; font-weight: bold;">${(user.sim * 100).toFixed(2)}%</span>
                            </p>
                            <p style="font-size: 13px; color: #666;">
                                共同偏好: ${user.intersection.join("、")}
                            </p>
                        </div>
                    `).join('');
                } else {
                    usersDiv.innerHTML = '<div class="no-result" style="padding: 20px;">暂无相似用户</div>';
                }
            }

            // ==========================================
            // 4. 显示共同偏好商品 A ∩ B (缺失的部分！)
            // ==========================================
            const commonList = document.getElementById('commonList');
            if (commonList) {
                // 从所有相似用户的 intersection 中提取商品并去重
                let commonItems = [];
                if (data.similar_users && data.similar_users.length > 0) {
                    let allIntersections = [];
                    data.similar_users.forEach(u => {
                        if (u.intersection && Array.isArray(u.intersection)) {
                            allIntersections = allIntersections.concat(u.intersection);
                        }
                    });
                    // 使用 Set 去重
                    commonItems = [...new Set(allIntersections)];
                }

                if (commonItems.length > 0) {
                    commonList.innerHTML = commonItems.map(item => 
                        buildProductCard(item, { badge: '共同' })
                    ).join('');
                } else {
                    commonList.innerHTML = '<div class="no-result"><span>📦</span>暂无共同偏好</div>';
                }
            }

            // ==========================================
            // 5. 显示推荐商品 (底部)
            // ==========================================
            const recList = document.getElementById("recList");
            if (recList) {
                if (data.recommendations && data.recommendations.length > 0) {
                    recList.innerHTML = data.recommendations.map(item => {
                        const itemName = (typeof item === 'object' && item !== null) 
                            ? (item.name || item.item || '未知商品') 
                            : item;
                        return buildProductCard({ name: itemName }, { badge: '推荐' });
                    }).join('');
                } else {
                    recList.innerHTML = '<div class="no-result"><span>🎁</span>暂无推荐商品</div>';
                }
            }
        })
        .catch(error => {
            console.error("请求失败:", error);
            const recList = document.getElementById("recList");
            if (recList) {
                recList.innerHTML = `<div class="no-result"><span>⚠️</span>推荐数据加载失败，请检查后端服务是否启动</div>`;
            }
        });
}