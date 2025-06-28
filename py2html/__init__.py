# my_website_project/py2html/__init__.py

import bs4
import sys

class Parent:
    def __init__(self):
        self.html = ""
        self.tags = list()
    
    def title(self, title):
        # Sets the title of the HTML document.
        self.title = str(title)
    
    def config(self, **kwargs):
        """
        Configures the Parent object with various attributes.
        Accepts keyword arguments for title, styles, etc.
        """
        if "title" in kwargs:
            self.title = str(kwargs["title"])
        
        if "style" in kwargs:
            if not isinstance(kwargs["style"], str):
                raise ValueError("Style must be a string.")
            self.style = str(kwargs["style"])
        
        # You can add more configurations as needed
        # For example, setting default styles or other properties

    
    def __call__(self, *args, escape=True, sep=" "):
        # This method allows the Parent to be called like a function, adding a text node.
        if args:
            self.TextNode(sep.join(args), escape=escape)
        return self.tags[-1]  # Return the last added button tag for further manipulation if needed
    
    def __delitem__(self, index):
        """
        Allows deletion of tags by index.
        This is useful for removing specific tags from the Parent.
        """
        if index < 0 or index >= len(self.tags):
            raise IndexError("Index out of range.")
        del self.tags[index]

    def __getitem__(self, index):
        """
        Allows indexing to retrieve tags.
        This is useful for accessing specific tags in the Parent.
        """
        if index < 0 or index >= len(self.tags):
            raise IndexError("Index out of range.")
        
        return self.tags[index]
        
    def save(self, destination):
        destination.write(self.getHTML(format=True))

    def saveToFile(self, filename):
        with open(filename, "w") as f:
            f.write(self.getHTML())

    def escapeCharacters(self, text):
        text = str(text)

        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&#39;")

        text = text.replace("\n", "<br>")
        text = text.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

        text = text.replace("c]", "</center>")
        text = text.replace("[c", "<center>")

        text = text.replace(" s]", "</span>")
        text = text.replace(" xs]", "</span>")
        text = text.replace(" xxs]", "</span>")
        text = text.replace(" l]", "</span>")
        text = text.replace(" xl]", "</span>")
        text = text.replace(" xxl]", "</span>")
        text = text.replace(" xxxl]", "</span>")
        text = text.replace(" m]", "</span>")
        text = text.replace("[xs ", "<span style='font-size: 0.6rem;'>")
        text = text.replace("[xxs ", "<span style='font-size: 0.4rem;'>")
        text = text.replace("[l ", "<span style='font-size: 1.2rem;'>")
        text = text.replace("[xl ", "<span style='font-size: 1.5rem;'>")
        text = text.replace("[xxl ", "<span style='font-size: 2rem;'>")
        text = text.replace("[xxxl ", "<span style='font-size: 3rem;'>")
        text = text.replace("[s ", "<span style='font-size: 0.8rem;'>")
        text = text.replace("[m ", "<span style='font-size: 1rem;'>")


        text = text.replace("`]", "</code>")
        text = text.replace("[`", "<code>")
        text = text.replace("```]", "</code></pre>")
        text = text.replace("[```", "<pre><code>")

        text = text.replace("*]", "</strong>")
        text = text.replace("_]", "</em>")
        text = text.replace("[*", "<strong>")
        text = text.replace("[_", "<em>")
        
        return text

    def getHTML(self, format=False, insideframe=False):
        self.html = ""
        
        self_closing_tags = ["img", "input", "br", "hr", "link", "meta", "area", "base", "col", "embed", "keygen", "param", "source", "track", "wbr"]

        if not insideframe:
            if format:
                self.html += "<html>\n<head>\n<title>Py2HTML Site</title>\n</head>\n<body style='padding: 0; margin: 0;'>\n"
            else:
                self.html += "<html><head><title>Py2HTML Site</title></head><body style='padding: 0; margin: 0;'>"

        for i in self.tags:
            if i["type"] == "textnode":
                # Text nodes are just raw text, no HTML tags
                self.html += i["content"]
                if format:
                    self.html += "\n"
                continue
            tag_type = i["type"]
            content = i.get("content", "")

            style_parts = []
            if i.get("fg"): style_parts.append(f"color: {i['fg']};")
            if i.get("bg"): style_parts.append(f"background: {i['bg']};")
            if i.get("bd"): style_parts.append(f"border: {i['bd']};")
            if i.get("bdr"): style_parts.append(f"border-radius: {i['bdr']};")
            if i.get("padding"): style_parts.append(f"padding: {i['padding'][1]}px {i['padding'][0]}px;")
            if i.get("width"): style_parts.append(f"width: {i['width']};")
            if i.get("height"): style_parts.append(f"height: {i['height']};")
            if i.get("margin"):
                style_parts.append(f"margin: {i['margin'][1]} {i['margin'][0]};")
            if i.get("text-decoration"): style_parts.append(f"text-decoration: {i['text-decoration']};")
            if i.get("display"):
                style_parts.append(f"display: {i['display']};")
                if i.get("display") == "flex" and "flex_config" in i:
                    flex_config = i["flex_config"]
                    style_parts.append(f"align-items: {flex_config.get('align-items', 'flex-start')};")
                    style_parts.append(f"justify-content: {flex_config.get('justify-content', 'flex-start')};")
                    style_parts.append(f"flex-direction: {flex_config.get('flex-direction', 'row')};")
                    style_parts.append(f"flex-wrap: {flex_config.get('flex-wrap', 'nowrap')};")
                    style_parts.append(f"gap: {flex_config.get('gap', '0px')};")
            if i.get("position"):
                style_parts.append(f"position: {i['position']};")
            if i.get("z-index"):
                style_parts.append(f"z-index: {i['z-index']};")
            if i.get("offset"):
                offset = i["offset"]
                style_parts.append(f"top: {offset.get('top', '0px')};")
                style_parts.append(f"left: {offset.get('left', '0px')};")
                style_parts.append(f"right: {offset.get('right', 'auto')};")
                style_parts.append(f"bottom: {offset.get('bottom', 'auto')};")

            # Join all style parts into a single string
            style_attr = f" style='{' '.join(style_parts)}'" if style_parts else ""

            other_attrs_list = []
            if "attrs" in i:
                for attr_key, attr_value in i["attrs"].items():
                    # Attribute values should always be escaped for security/correctness
                    other_attrs_list.append(f'{attr_key}="{self.escapeCharacters(str(attr_value))}"')
            
            # Specific attributes for Image and Script tags that might also be in attrs
            if tag_type == "img":
                if i.get("src"): other_attrs_list.append(f'src="{self.escapeCharacters(str(i["src"]))}"')
                if i.get("alt"): other_attrs_list.append(f'alt="{self.escapeCharacters(str(i["alt"]))}"')
            elif tag_type == "script" and i.get("src"): # Script's src attribute
                other_attrs_list.append(f'src="{self.escapeCharacters(str(i["src"]))}"')


            attrs_str = style_attr + (" " + " ".join(other_attrs_list) if other_attrs_list else "")

            # --- IMPORTANT: Special handling for <script> content ---
            if tag_type == "script":
                # The content of a script tag (the JavaScript code) should NOT be escaped.
                # It's already stored raw in the Script method.
                addition = f"""<{tag_type}{attrs_str}>{content}</{tag_type}>"""
            elif tag_type in self_closing_tags:
                addition = f"""<{tag_type}{attrs_str} />"""
            else:
                # For all other tags, content is assumed to be either escaped string or raw HTML from nested Parent
                if isinstance(content, list):
                    newcontent = Parent()
                    newcontent.tags=content
                    addition = f"""<{tag_type}{attrs_str}>{newcontent.getHTML(insideframe=1)}</{tag_type}>"""
                else:
                    addition = f"""<{tag_type}{attrs_str}>{content}</{tag_type}>"""

            self.html += addition
            if format:
                self.html += "\n"

        if not insideframe:
            if format:
                self.html += "</body>\n</html>"
            else:
                self.html += "</body></html>"

        result_html = self.html

        if format:
            try:
                soup = bs4.BeautifulSoup(result_html, "html.parser")
                result_html = soup.prettify()
            except Exception as e:
                pass

        return result_html

    def Button(self, fg="#00a651", bg="#deffee", bd="none", bdradius="50px", text="Py2HTML", padx=15, pady=15):
        escaped_text = self.escapeCharacters(str(text))
        self.tags.append({"type": "button", "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":escaped_text, "padding":(padx,pady)})
        return len(self.tags) - 1

    def Label(self, fg="#000", bg="#fff", bd="none", bdradius="50px", text="Py2HTML", padx=15, pady=15):
        escaped_text = self.escapeCharacters(str(text))
        self.tags.append({"type": "p", "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":escaped_text, "padding":(padx,pady)})
        return len(self.tags) - 1

    def Text(self, fg="#000", bg="#deffee", bd="none", bdradius="50px", text="Py2HTML", padx=15, pady=15):
        escaped_text = self.escapeCharacters(str(text))
        self.tags.append({"type": "textarea", "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":escaped_text, "padding":(padx,pady)})
        return len(self.tags) - 1

    def Frame(self, fg="#000", bg="#fff", bd="none", bdradius="50px", content="Py2HTML", padx=15, pady=15, width="auto", height="auto", marginx=0, marginy=0, content_manager="block", flex_config={"align-items": "flex-start", "justify-content": "flex-start", "flex-direction": "row", "flex-wrap": "nowrap", "gap": "0px"}, position="static", offset={"top": "0px", "left": "0px", "right": "auto", "bottom": "auto"}):
        if isinstance(content, Parent):
            self.tags.append({"type": "div", "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":content.tags, "padding":(padx,pady), "width":width, "height":height, "margin":(str(marginx), str(marginy)), "display": content_manager, "flex_config": flex_config, "position": position, "offset": offset})
        else:
            self.tags.append({"type": "div", "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":self.escapeCharacters(str(content)), "padding":(padx,pady), "width":width, "height":height, "margin":(str(marginx), str(marginy)), "display": content_manager, "flex_config": flex_config, "position": position, "offset": offset})
        # Note: The content is escaped if it's a string, but if it's a Parent, it will be rendered as HTML inside the div.
        return len(self.tags) - 1

    def Heading(self, level=1, text="Py2HTML Heading", fg="#333", bg="transparent", bd="none", bdradius="0px", padx=0, pady=0):
        if not 1 <= level <= 6:
            raise ValueError("Heading level must be between 1 and 6.")
        tag_type = f"h{level}"
        escaped_text = self.escapeCharacters(str(text))
        self.tags.append({"type": tag_type, "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":escaped_text, "padding":(padx,pady)})
        return len(self.tags) - 1

    def Image(self, src="", alt="", width=None, height=None, bd="none", bdradius="0px"):
        image_data = {
            "type": "img",
            "src": src,
            "alt": alt,
            "bd":str(bd),
            "bdr":str(bdradius)
        }
        if width is not None:
            image_data["width"] = width
        if height is not None:
            image_data["height"] = height
        self.tags.append(image_data)
        return len(self.tags) - 1
   
    def Link(self, href="https://example.com", text="Click Here", fg="#00a651", bg="transparent", bd="none", bdradius="0px", padx=0, pady=0, text_decor="underline"):
        escaped_text = self.escapeCharacters(str(text))
        self.tags.append({"type": "a", "attrs": {"href":href}, "fg":str(fg), "bg":str(bg), "bd":str(bd), "bdr":str(bdradius), "content":escaped_text, "padding":(padx,pady), "text-decoration": text_decor})
        return len(self.tags) - 1

    def CustomTag(self, tag_name="div", content="", fg=None, bg=None, bd=None, bdradius=None, padx=None, pady=None, **kwargs):
        final_content = ""
        if isinstance(content, Parent):
            final_content = content.tags
        else:
            final_content = self.escapeCharacters(str(content))

        tag_data = {
            "type": tag_name,
            "content": final_content,
            "attrs": kwargs
        }
        if fg is not None: tag_data["fg"] = str(fg)
        if bg is not None: tag_data["bg"] = str(bg)
        if bd is not None: tag_data["bd"] = str(bd)
        if bdradius is not None: tag_data["bdr"] = str(bdradius)
        if padx is not None and pady is not None: tag_data["padding"] = (padx, pady)
        elif padx is not None or pady is not None:
             print("Warning: Only one of padx/pady provided for CustomTag. Padding may not apply as expected.", file=sys.stderr)

        self.tags.append(tag_data)
        return len(self.tags) - 1

    def TextNode(self, text="", escape=True):
        """
        Adds a text node to the HTML.
        This is useful for adding plain text without any HTML tags.
        """
        if escape: escaped_text = self.escapeCharacters(str(text))
        else: escaped_text = str(text)
        self.tags.append({"type": "textnode", "content": escaped_text})
        return len(self.tags) - 1
    
    # --- NEW: Script function for JavaScript integration ---
    def Script(self, code="", src=None, **kwargs):
        """
        Adds a <script> tag to the HTML.
        Use 'code' for inline JavaScript, or 'src' for an external JavaScript file.
        'src' takes precedence if both are provided.
        Additional kwargs are passed as attributes (e.g., async=True, defer=True, type="module").
        """
        if src and code:
            print("Warning: Both 'code' and 'src' provided for Script. 'src' will take precedence.", file=sys.stderr)
            code = "" # Clear inline code if src is present

        tag_data = {
            "type": "script",
            "attrs": kwargs # For attributes like 'async', 'defer', 'type'
        }
        if src:
            # The 'src' attribute value should still be escaped as it's a URL/path
            tag_data["src"] = self.escapeCharacters(str(src)) 
        
        # The content of the script tag (the JS code itself) is stored raw.
        # getHTML will ensure this content is not escaped when rendered.
        tag_data["content"] = str(code) 
        
        self.tags.append(tag_data)
        return len(self.tags) - 1
    
    def __str__(self):
        return self.getHTML(format=True, insideframe=False)