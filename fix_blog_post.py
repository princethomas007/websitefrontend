# -*- coding: utf-8 -*-
import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog-post.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hero section to be dynamic
hero_regex = re.compile(r'<div class="page-hero">.*?</div>', re.DOTALL)
new_hero = '''<div class="page-hero" style="min-height:40vh; padding-top: 150px; padding-bottom: 50px;">
        <div class="page-hero-bg reveal"></div>
        <div class="page-hero-badge reveal rd1" id="postCategory">Loading...</div>
        <h1 class="reveal rd2 hero-custom-title" id="postTitle" style="font-size: 3rem !important; opacity:1 !important; transform:none !important; filter:none !important; animation:none !important;">
            Loading Title...
        </h1>
        <p class="rd3 hero-custom-sub" id="postMeta" style="opacity:1 !important; transform:none !important; filter:none !important; animation:none !important; margin-bottom: 30px;">
            By Rextech Studios
        </p>
    </div>'''

content = re.sub(hero_regex, new_hero, content)

# Replace the blog section to have an article tag instead of a grid
blog_section_regex = re.compile(r'<section class="section blog-section".*?</section>', re.DOTALL)
new_blog_section = '''<section class="section blog-section" style="background:var(--black); padding-top: 20px;">
        <div class="blog-content reveal rd1">
            <div class="max-w" style="max-width: 800px; margin: 0 auto;">
                <div id="postImage" style="width: 100%; border-radius: 20px; overflow: hidden; margin-bottom: 40px; border: 1px solid rgba(255,255,255,0.1);">
                    <!-- Image inserted via JS -->
                </div>
                <div id="postContent" style="color: #ccc; font-size: 1.1rem; line-height: 1.8;">
                    Loading content...
                </div>
                <div style="margin-top: 60px;">
                    <a href="blog.html" class="btn btn-primary" style="background: var(--purple-primary); border: none; padding: 12px 24px; border-radius: 30px; color: #fff; text-decoration: none;">&larr; Back to Blogs</a>
                </div>
            </div>
        </div>
    </section>'''

content = re.sub(blog_section_regex, new_blog_section, content)

# Replace the JS logic at the bottom
js_regex = re.compile(r'<script>\s*fetch\("https://rextech-django-production.up.railway.app/api/blog/"\).*?</script>', re.DOTALL)
new_js = '''<script>
      const urlParams = new URLSearchParams(window.location.search);
      const blogId = urlParams.get('id');

      if (!blogId) {
          document.getElementById("postTitle").innerText = "Blog Post Not Found";
          document.getElementById("postContent").innerHTML = "<p>Invalid link. Please return to the blog page.</p>";
      } else {
          fetch("https://rextech-django-production.up.railway.app/api/blog/")
            .then(response => response.json())
            .then(blogs => {
              const blog = blogs.find(b => b.id == blogId);
              
              if (!blog) {
                  document.getElementById("postTitle").innerText = "Blog Post Not Found";
                  document.getElementById("postContent").innerHTML = "<p>We couldn't find this post.</p>";
                  return;
              }

              // Set Title & Category
              document.getElementById("postTitle").innerText = blog.title;
              document.getElementById("postCategory").innerText = blog.category || "Blog";

              // Set Meta
              const date = new Date(blog.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
              document.getElementById("postMeta").innerText = By  | ;

              // Set Image
              const imageUrl = blog.image && blog.image.startsWith("http")
                ? blog.image
                : https://rextech-django-production.up.railway.app;
              
              if (blog.image) {
                  document.getElementById("postImage").innerHTML = <img src="" alt="" style="width: 100%; height: auto; display: block;">;
              }

              // Set Content (Formatting newlines to paragraphs)
              const formattedContent = blog.content ? blog.content.replace(/\\n/g, '<br>') : "No content available.";
              document.getElementById("postContent").innerHTML = formattedContent;
            })
            .catch(err => {
                console.error("Blog fetch error:", err);
                document.getElementById("postTitle").innerText = "Error Loading Post";
                document.getElementById("postContent").innerHTML = "<p>Please try again later.</p>";
            });
      }
    </script>'''

content = re.sub(js_regex, new_js, content)

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog-post.html', 'w', encoding='utf-8') as f:
    f.write(content)
