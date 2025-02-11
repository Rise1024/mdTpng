#!/usr/bin/env python3
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import re
from playwright.sync_api import sync_playwright

# 配置参数
# Update CONFIG with new styling parameters
# Update CONFIG with carbon_style settings
CONFIG = {
    "output_dir": "output_images",  # 输出图片的目录
    "image_size": {"width": 1080, "height": 1920},  # 图片的宽度和高度
    "theme": {
        "background": "#a6b2bd",  # 背景颜色
        "text_color": "#e6e6e6",  # 文字颜色
        "code_theme": "monokai",  # 代码高亮主题
        "font_family": "'LXGW WenKai Screen', sans-serif",  # 字体家族
        "font_import": "@import url('https://cdn.staticfile.org/lxgw-wenkai-screen-webfont/1.6.0/lxgwwenkaiscreen.css');",  # 字体导入
        "watermark": "东升Coding",  # 水印文字
        "decorative_elements": True,  # 是否启用装饰元素
        "carbon_style": {
            "padding": "48px",  # 内边距
            "border_radius": "10px",  # 边框圆角
            "shadow": "rgba(0, 0, 0, 0.55) 0px 8px 24px"  # 阴影效果
        }
    }
}

def parse_markdown(filename):
    """解析Markdown文件为封面和多个主题片段"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # 按一级标题分割内容，第一部分作为封面
    sections = re.split(r'(?=\n#\s+)', content)
    cover = sections[0].strip() if sections else ""
    
    # 确保封面包含第一个一级标题及其内容
    if len(sections) > 1:
        cover = sections[0] + sections[1]
    
    # 按二级标题分割内容
    content_sections = re.split(r'(?=\n##\s+)', content)
    return cover, [s.strip() for s in content_sections if s.strip()]

def md_to_images(md_file):
    """主转换函数"""
    os.makedirs(CONFIG['output_dir'], exist_ok=True)
    cover, sections = parse_markdown(md_file)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=CONFIG['image_size'])
        
        # 生成封面图片
        cover_html = generate_html(cover)  # 使用与内容相同的HTML生成函数
        page.set_content(cover_html)
        page.wait_for_load_state('networkidle')
        page.screenshot(path=os.path.join(CONFIG['output_dir'], "cover.png"), full_page=True)
        
        # 生成内容图片
        for i, section in enumerate(sections):
            html = generate_html(section)
            page.set_content(html)
            page.wait_for_load_state('networkidle')
            
            # Get the actual content height
            content_height = page.evaluate('''() => {
                const body = document.body;
                const html = document.documentElement;
                return Math.max(
                    body.scrollHeight, body.offsetHeight,
                    html.clientHeight, html.scrollHeight, html.offsetHeight
                );
            }''')
            
            # Adjust viewport height based on content
            min_height = 800  # Minimum height
            max_height = CONFIG['image_size']['height']  # Maximum height
            adjusted_height = min(max(content_height + 100, min_height), max_height)
            
            # Update page viewport
            page.set_viewport_size({
                'width': CONFIG['image_size']['width'],
                'height': adjusted_height
            })
            
            output_path = os.path.join(CONFIG['output_dir'], f"note_{i+1:02d}.png")
            page.screenshot(path=output_path, full_page=True)
        
        browser.close()

def generate_cover_html(content):
    """生成封面HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #a6b2bd, #3f72af);
                display: flex;
                justify-content: center;
                align-items: center;
                color: #ffffff;
                font-family: {CONFIG['theme']['font_family']};
            }}
            .cover-title {{
                font-size: 64px;
                text-align: center;
                text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }}
        </style>
    </head>
    <body>
        <div class="cover-title">
            {markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])}
        </div>
    </body>
    </html>
    """

def generate_html(content):
    formatter = HtmlFormatter(style=CONFIG['theme']['code_theme'])
    css_code = formatter.get_style_defs('.highlight')
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            {CONFIG['theme']['font_import']}
            body {{
                margin: 0;
                padding: 50px;
                min-height: 100vh;
                width: 100%;
                background: #a6b2bd;
                color: {CONFIG['theme']['text_color']};
                font-family: {CONFIG['theme']['font_family']};
                line-height: 1.6;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 22px;  /* 再次增大字体大小 */
            }}
            
            .content {{
                background: #151718;
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                position: relative;
                backdrop-filter: blur(10px);
                max-width: 980px;
                width: 100%;
                word-wrap: break-word;
                overflow-wrap: break-word;
                font-size: 22px;  /* 再次增大字体大小 */
            }}
            
            /* 标题样式增强 */
            h1, h2 {{
                font-size: 52px !important;  /* 再次增大字体大小 */
            }}
            
            h3 {{
                font-size: 40px !important;  /* 再次增大字体大小 */
            }}
            
            h4 {{
                font-size: 34px !important;  /* 再次增大字体大小 */
            }}
            
            h5 {{
                font-size: 28px !important;  /* 再次增大字体大小 */
            }}
            
            h6 {{
                font-size: 26px !important;  /* 再次增大字体大小 */
            }}
            
            /* Carbon-style window controls */
            .window-controls {{
                position: absolute;
                top: 12px;
                left: 16px;
                height: 12px;
                width: 52px;
                display: flex;
                gap: 8px;
            }}
            
            .window-control {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
            }}
            
            .window-control.close {{ background: #ff5f56; }}
            .window-control.minimize {{ background: #ffbd2e; }}
            .window-control.maximize {{ background: #27c93f; }}
            
            /* 标题样式增强 */
            h1, h2 {{
                color: #7ec4ff;
                letter-spacing: 1px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                text-align: center;
                font-size: 42px !important;
                border-bottom: 3px solid #3f72af;
                padding-bottom: 15px;
            }}
            
            h3, h4, h5, h6 {{
                color: #7ec4ff;
                letter-spacing: 1px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                text-align: left;
            }}
            
            h2 {{
                font-size: 36px !important;
                border-bottom: 2px solid #3f72af;
                padding-bottom: 12px;
            }}
            
            h3 {{
                font-size: 30px !important;
                color: #6db4ff;
            }}
            
            h4 {{
                font-size: 24px !important;
                color: #5ba8ff;
            }}
            
            h5 {{
                font-size: 20px !important;
                color: #4a9eff;
            }}
            
            h6 {{
                font-size: 18px !important;
                color: #3994ff;
            }}
            
            /* 标题悬停效果 */
            h1:hover, h2:hover, h3:hover, h4:hover, h5:hover, h6:hover {{
                transform: translateX(5px);
                transition: transform 0.3s ease;
            }}
            {css_code}
            /* Decorative elements */
            .content::before {{
                content: '';
                position: absolute;
                top: -10px;
                left: -10px;
                right: -10px;
                bottom: -10px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 30px;
                z-index: -1;
            }}
            /* Watermark style */
            .watermark {{
                position: fixed;
                bottom: 30px;
                right: 40px;
                font-size: 14px;
                opacity: 0.5;
                color: #7ec4ff;
                transform: rotate(-15deg);
            }}
            /* Enhanced typography */
            h2 {{
                color: #7ec4ff;
                border-bottom: 2px solid #3f72af;
                padding-bottom: 12px;
                font-size: 32px !important;
                margin-top: 0;
                letter-spacing: 1px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
                font-weight: 600;
                margin-bottom: 24px;
            }}
            blockquote {{
                border-left: 4px solid #3f72af;
                margin: 20px 0;
                padding: 15px 30px;
                background: rgba(255, 255, 255, 0.03);
                color: #a8d0ff;
            }}
            table {{
                border-collapse: collapse;
                margin: 25px 0;
                box-shadow: 0 0 20px rgba(0,0,0,0.15);
                width: 100%;
            }}
            th, td {{
                padding: 15px;
                border: 1px solid #364f6b;
                text-align: left;
            }}
            th {{
                background-color: #16213e;
                color: #7ec4ff;
            }}
            tr:nth-child(even) {{
                background-color: rgba(255, 255, 255, 0.03);
            }}
            /* Add decorative quote marks for blockquotes */
            blockquote::before {{
                content: '"';
                font-size: 60px;
                color: rgba(126, 196, 255, 0.2);
                position: absolute;
                left: 10px;
                top: -10px;
            }}
            
            /* Enhanced code blocks */
            pre {{ 
                padding: 25px;
                border-radius: 12px;
                overflow-x: auto;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            /* Add subtle animation for hover effects */
            pre:hover {{
                border-color: rgba(126, 196, 255, 0.3);
                transition: all 0.3s ease;
            }}
            
            /* Carbon-style code blocks */
            .code-wrapper {{
                position: relative;
                margin: 2em 0;
            }}
            
            .window-controls {{
                position: absolute;
                top: 12px;
                left: 16px;
                height: 12px;
                width: 52px;
                display: flex;
                gap: 8px;
            }}
            
            .window-control {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
            }}
            
            .window-control.close {{ background: #ff5f56; }}
            .window-control.minimize {{ background: #ffbd2e; }}
            .window-control.maximize {{ background: #27c93f; }}
            
            pre {{
                position: relative;
                padding: {CONFIG['theme']['carbon_style']['padding']};
                padding-top: 56px;
                border-radius: {CONFIG['theme']['carbon_style']['border_radius']};
                background: #1a1b1f;
                box-shadow: {CONFIG['theme']['carbon_style']['shadow']};
                margin: 2em 0;
            }}
            
            code {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                line-height: 1.5;
            }}
            
            /* 增强图片样式 */
            img {{
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                max-width: 100%;
                height: auto;
            }}
            
            /* 增强链接样式 */
            a {{
                color: #7ec4ff;
                text-decoration: none;
                border-bottom: 1px dashed rgba(126, 196, 255, 0.4);
                transition: all 0.3s ease;
            }}
            
            a:hover {{
                border-bottom-color: #7ec4ff;
            }}
        </style>
    </head>
    <body>
        <div class="window-controls">
            <div class="window-control close"></div>
            <div class="window-control minimize"></div>
            <div class="window-control maximize"></div>
        </div>
        <div class="outer-container">
            <div class="content">
                {markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])}
            </div>
        </div>
        <div class="watermark">{CONFIG['theme']['watermark']}</div>
        <script>
            // 为所有代码块添加窗口控制按钮
            document.querySelectorAll('pre').forEach(pre => {{
                const wrapper = document.createElement('div');
                wrapper.className = 'window-controls';
                wrapper.innerHTML = `
                    <div class="window-control close"></div>
                    <div class="window-control minimize"></div>
                    <div class="window-control maximize"></div>
                `;
                pre.insertBefore(wrapper, pre.firstChild);
            }});
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    md_to_images("/Users/ht/VSCode/mdTnpg/technical_notes.md")