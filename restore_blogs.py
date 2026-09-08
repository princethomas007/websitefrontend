import re

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The static cards block to restore (exactly as they were before)
static_cards = '''                    <div class="card blog-card">
                        <div class="blog-img">
                            <img src="./assets/images/metaverse1.jpg" alt="Metaverse">
                        </div>
                        <div class="blog-body">
                            <span class="blog-tag">Metaverse</span>
                            <h3 class="blog-title">Metaverse in 2025: Opportunities for Businesses</h3>
                            <p class="blog-excerpt">How businesses are leveraging metaverse technologies to create new
                                revenue streams, engage customers, and build virtual presences.</p>
                            <div class="blog-meta"><span>Rextech Studios</span><span>2025</span></div>
                            <span class="blog-read">Read more &#8594;</span>
                        </div>
                    </div>
                    <div class="card blog-card">
                        <div class="blog-img">
                            <img src="./assets/images/Unity_vs_Unreal2.jpg" alt="Unity_vs_Unreal">
                        </div>
                        <div class="blog-body">
                            <span class="blog-tag">Game Development</span>
                            <h3 class="blog-title">Unity vs Unreal: Which Engine is Right for Your Project?</h3>
                            <p class="blog-excerpt">A comprehensive comparison of Unity and Unreal Engine covering
                                performance, pricing, community, and use-case fit for different game types.</p>
                            <div class="blog-meta"><span>Rextech Studios</span><span>2025</span></div>
                            <span class="blog-read">Read more &#8594;</span>
                        </div>
                    </div>
                    <div class="card blog-card">
                        <div class="blog-img">
                            <img src="./assets/images/AR_Business3.jpg" alt="AR VR">
                        </div>
                        <div class="blog-body">
                            <span class="blog-tag">AR/VR</span>
                            <h3 class="blog-title">How AR is Transforming Retail and Real Estate</h3>
                            <p class="blog-excerpt">Augmented reality is changing how customers experience products
                                before buying from furniture placement to virtual property tours.</p>
                            <div class="blog-meta"><span>Rextech Studios</span><span>2025</span></div>
                            <span class="blog-read">Read more &#8594;</span>
                        </div>
                    </div>
                    <div class="card blog-card">
                        <div class="blog-img">
                            <img src="./assets/images/Flutter_vs_React4.jpg" alt="Flutter_vs_React">
                        </div>
                        <div class="blog-body">
                            <span class="blog-tag">Mobile Apps</span>
                            <h3 class="blog-title">Flutter vs React Native: Building Cross-Platform Apps in 2025</h3>
                            <p class="blog-excerpt">Our engineers compare Flutter and React Native based on real-world
                                projects - performance, developer experience, and ecosystem maturity.</p>
                            <div class="blog-meta"><span>Rextech Studios</span><span>2025</span></div>
                            <span class="blog-read">Read more &#8594;</span>
                        </div>
                    </div>
                    <div class="card blog-card">
                        <div class="blog-img">
                            <img src="./assets/images/game_career5.jpg" alt="game_career">
                        </div>
                        <div class="blog-body">
                            <span class="blog-tag">Career</span>
                            <h3 class="blog-title">How to Start a Career in Game Development: A Complete Guide</h3>
                            <p class="blog-excerpt">Everything you need to know about breaking into the game industry -
                                skills, tools, portfolio building, and landing your first role.</p>
                            <div class="blog-meta"><span>Rextech Studios</span><span>2025</span></div>
                            <span class="blog-read">Read more &#8594;</span>
                        </div>
                    </div>
                    <div class="card blog-card">
                        <div class="blog-img">
                            <img src="./assets/images/AI_game6.jpg" alt="AI_game">
                        </div>
                        <div class="blog-body">
                            <span class="blog-tag">AI &amp; Innovation</span>
                            <h3 class="blog-title">AI in Game Development: Tools That Are Changing Everything</h3>
                            <p class="blog-excerpt">From AI-generated assets to adaptive NPC behaviour - how artificial
                                intelligence is reshaping modern game development pipelines.</p>
                            <div class="blog-meta"><span>Rextech Studios</span><span>2025</span></div>
                            <span class="blog-read">Read more &#8594;</span>
                        </div>
                    </div>'''

# Replace the empty dynamicBlog grid with one that has static cards + dynamic append
# The JS will simply append new API cards to the same grid
old_grid = '<div id="dynamicBlog" class="grid-3 reveal"></div>'
new_grid = '''<div id="dynamicBlog" class="grid-3 reveal">
''' + static_cards + '''
                </div>'''

content = content.replace(old_grid, new_grid, 1)

with open(r'C:\Users\SMRITHI\Desktop\websitefrontend\blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done - static cards restored!")
