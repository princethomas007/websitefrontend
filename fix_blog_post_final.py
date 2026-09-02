# -*- coding: utf-8 -*-
import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog-post.html', 'r', encoding='utf-8') as f:
    content = f.read()

js_regex = re.compile(r'<script>\s*const urlParams = new URLSearchParams.*?</script>', re.DOTALL)
new_js = '''<script>
      const urlParams = new URLSearchParams(window.location.search);
      const blogId = urlParams.get('id');

      if (!blogId) {
          document.getElementById("postTitle").innerText = "Blog Post Not Found";
          document.getElementById("postContent").innerHTML = "<p>No blog ID provided in the URL. Please go back to the blog page.</p>";
          document.getElementById("postCategory").innerText = "Error";
          document.getElementById("postMeta").innerText = "";
      } else {
          fetch("https://rextech-django-production.up.railway.app/api/blog/")
            .then(response => response.json())
            .then(blogs => {
              const blog = blogs.find(b => b.id == blogId);
              
              if (!blog) {
                  document.getElementById("postTitle").innerText = "Blog Post Not Found";
                  document.getElementById("postContent").innerHTML = "<p>We couldn't find this post.</p>";
                  document.getElementById("postCategory").innerText = "Error";
                  return;
              }

              // Set Title & Category
              document.getElementById("postTitle").innerText = blog.title;
              document.getElementById("postCategory").innerText = blog.category || "Blog";

              // Set Meta
              const date = new Date(blog.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
              document.getElementById("postMeta").innerText = `By ${blog.author || "Rextech Studios"} | ${date}`;

              // Set Image
              const imageUrl = blog.image && blog.image.startsWith("http")
                ? blog.image
                : `https://rextech-django-production.up.railway.app${blog.image}`;
              
              if (blog.image) {
                  document.getElementById("postImage").innerHTML = `<img src="${imageUrl}" alt="${blog.title}" style="width: 100%; height: auto; display: block; object-fit: cover;">`;
              }

              // Set Content - preserving paragraphs!
              if (blog.content) {
                  // split by double newlines or single newlines and wrap in <p>
                  const paragraphs = blog.content.split(/\\n+/).filter(p => p.trim() !== '');
                  const formattedContent = paragraphs.map(p => `<p style="margin-bottom: 20px;">${p}</p>`).join('');
                  document.getElementById("postContent").innerHTML = formattedContent;
              } else {
                  document.getElementById("postContent").innerHTML = "<p>No content available.</p>";
              }
            })
            .catch(err => {
                console.error("Blog fetch error:", err);
                document.getElementById("postTitle").innerText = "Error Loading Post";
                document.getElementById("postContent").innerHTML = "<p>Please try again later. The server might be asleep.</p>";
            });
      }
    </script>'''

content = re.sub(js_regex, new_js, content)

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog-post.html', 'w', encoding='utf-8') as f:
    f.write(content)
