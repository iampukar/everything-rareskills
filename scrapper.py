import asyncio
from playwright.async_api import async_playwright

async def fetch_blog_posts(page):
    await page.goto("https://www.rareskills.io/blog")

    last_scroll_height = 0
    current_scroll_height = await page.evaluate("document.body.scrollHeight")

    print("Wait! Determining the total scroll height...")
    while last_scroll_height < current_scroll_height:
        last_scroll_height = current_scroll_height
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(4000)
        current_scroll_height = await page.evaluate("document.body.scrollHeight")
    print("Total scroll height check completed!")
    
    posts = await page.evaluate('''() => {
        const items = Array.from(document.querySelectorAll('.iSTCpN.TBrkhx.post-list-item-wrapper.blog-post-homepage-description-font.blog-post-homepage-description-color.blog-post-homepage-description-fill'));
        return items.map(item => {
            const titleElement = item.querySelector('.T5UMT5.fcPJ4D.blog-hover-container-element-color.WD_8WI.post-title.blog-post-homepage-title-color.blog-post-homepage-title-font');
            const authorElement = item.querySelector('.tQ0Q1A.user-name.mJ89ha.blog-post-homepage-description-color.blog-post-homepage-description-font.blog-post-homepage-link-hashtag-hover-color');
            const dateElement = item.querySelector('.post-metadata__date.time-ago');
            const readTimeElement = item.querySelector('.post-metadata__readTime');
            const linkElement = item.querySelector('a');

            return {
                title: titleElement?.innerText,
                author: authorElement?.innerText,
                published_date: dateElement?.innerText,
                reading_time: readTimeElement?.innerText,
                link: linkElement?.href,
            };
        });
    }''')
    return posts

def generate_readme(posts):
    readme_content = "# Everything Rareskills\n\n"
    readme_content += "This README file includes all the [blog posts](https://www.rareskills.io/blog) references from Rareskills.\n\n"
    readme_content += "## Getting Started\n\n"
    readme_content += "To set up the project, run the following commands:\n\n"
    readme_content += "```bash\n"
    readme_content += "chmod +x setup.sh\n"
    readme_content += "./setup.sh\n"
    readme_content += "```\n\n"
    readme_content += "| Title | Author | Published Date | Reading Time | Link | Read |\n"
    readme_content += "|-------|--------|----------------|--------------|------|------|\n"

    for post in posts:
        read_status = "[ ]"  # All posts are unread by default
        readme_content += f"| {post['title']} | {post['author']} | {post['published_date']} | {post['reading_time']} | [Link]({post['link']}) | {read_status} |\n"

    with open("README.md", "w") as f:
        f.write(readme_content)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        posts = await fetch_blog_posts(page)
        generate_readme(posts)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())