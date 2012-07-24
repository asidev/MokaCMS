<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.google.com/schemas/sitemap/0.84" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.google.com/schemas/sitemap/0.84 http://www.google.com/schemas/sitemap/0.84/sitemap.xsd">
	% for page in pages:
		<url>
			<loc>${request.host_url}${page.url}</loc>
			% if hasattr(page, "sitemap"):
			% for opt in page.sitemap:
			% if page.sitemap[opt]:
			<${opt}>${page.sitemap[opt]}</${opt}>
			% endif
			% endfor
			% endif
		</url>
	% endfor
</urlset>

