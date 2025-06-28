# py2html installer
# py2html is not on pip, so we need to install it manually

import os
import pathlib
import sys
from tkinter import *
from tkinter import messagebox, filedialog, ttk
import subprocess
import threading
from pathlib import Path
import asyncio


# stop blurry tkinter window on high DPI displays
if sys.platform == "win32":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)  # 1 = PROCESS_SYSTEM_DPI_AWARE
    except ImportError:
        pass

def install_py2html(gui, path=(Path.home() / 'py2html')):
    # py2html is not on pip, so we need to install it manually
    # install dependencies using pip

    subprocess.call(
                    [sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'],
                    stdout=sys.stdout,
                    stderr=subprocess.PIPE
                )

    
    p.title("Installing...")

    path.mkdir(exist_ok=1)
    f = (path / "__init__.py").open("w+")
    f.write(
        '''import bs4
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

        text = text.replace("\\\n", "<br>")
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
                self.html += "<html>\\\n<head>\\\n<title>Py2HTML Site</title>\\\n</head>\\\n<body style='padding: 0; margin: 0;'>\\\n"
            else:
                self.html += "<html><head><title>Py2HTML Site</title></head><body style='padding: 0; margin: 0;'>"

        for i in self.tags:
            if i["type"] == "textnode":
                # Text nodes are just raw text, no HTML tags
                self.html += i["content"]
                if format:
                    self.html += "\\\n"
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
                self.html += "\\\n"

        if not insideframe:
            if format:
                self.html += "</body>\\\n</html>"
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
        '''
    )

    f.close()

    if gui():
        g = (path / "py2htmlGUI.py").open("w+")
        g.write('''from tkinter import *
import py2html 
import json
from tkinter import ttk, font
from tkinter import filedialog
from ctypes import windll
from tkinterweb import HtmlFrame
from tkinter import messagebox
import copy
import webview
import sv_ttk



# Set DPI awareness for better scaling on Windows
windll.shcore.SetProcessDpiAwareness(1)

# --- Global Variables for GUI State ---
treeview_item_to_py2html_parent_map = {}
html = None
current_py2html_target_parent = None
current_treeview_parent_id = ""
treeviewer = None
status_bar_label = None


# --- Helper Functions for Managing py2html.Parent objects and their JSON serialization ---

def _recursively_reconstruct_py2html_objects(json_data_list):
    """
    Recursively reconstructs the in-memory py2html.Parent objects and their tag structures
    from a JSON-loaded list of dictionaries.
    
    This function creates new py2html.Parent objects for containers (like 'div' tags)
    and populates their 'tags' list with the deserialized children.
    
    Crucially, for 'div' tags, it sets their 'content' key in the in-memory tag dictionary
    to the *py2html.Parent object itself* that manages its children.
    This allows the GUI to easily access the child manager.
    """
    reconstructed_tags = []
    for tag_dict in json_data_list:
        reconstructed_tag_copy = copy.deepcopy(tag_dict)
        
        # If it's a div and its content is a list (as it would be after JSON load)
        if reconstructed_tag_copy.get('type') == 'div' and isinstance(reconstructed_tag_copy.get('content'), list):
            # Create a new py2html.Parent object to manage these children
            nested_parent_manager = py2html.Parent()
            
            # Recursively reconstruct the children and assign the result to the new manager's tags
            nested_parent_manager.tags = _recursively_reconstruct_py2html_objects(reconstructed_tag_copy['content'])
            
            # Replace the 'content' list in the div's dictionary with the actual Parent object
            # This is how the GUI will maintain its reference to the children manager
            reconstructed_tag_copy['content'] = nested_parent_manager 
            
        reconstructed_tags.append(reconstructed_tag_copy)
    return reconstructed_tags


# --- Main GUI Window Function ---
def newwindow():
    global current_py2html_target_parent, current_treeview_parent_id, html, treeviewer, treeview_item_to_py2html_parent_map, status_bar_label

    # Initialize / Reset for a new project
    html = py2html.Parent()
    treeview_item_to_py2html_parent_map.clear()
    
    current_py2html_target_parent = html
    current_treeview_parent_id = "" 
    treeview_item_to_py2html_parent_map[""] = html 


    r = Tk()
    r.geometry("800x700") 
    r.title("Py2HTML GUI")
    current_dpi_scale_factor = r.winfo_fpixels('1i') / 72
    r.tk.call('tk', 'scaling', current_dpi_scale_factor)
    r.option_add("*Font", ("Segoe UI", " 10"))


    # --- Treeview and Scrollbars ---
    tree_frame = Frame(r)
    tree_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    treeviewer = ttk.Treeview(tree_frame, columns=('Tag Type',), show='tree')
    treeviewer.heading('#0', text='Element Hierarchy', anchor=W)
    treeviewer.pack(side=LEFT, fill=BOTH, expand=True)

    tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=treeviewer.yview)
    tree_scrollbar.pack(side=RIGHT, fill=Y)
    treeviewer.config(yscrollcommand=tree_scrollbar.set)

    # --- Status Bar ---
    status_bar_label = ttk.Label(r, text="Inserting into: (Root Document)", relief=SUNKEN, anchor="w")
    status_bar_label.pack(side=BOTTOM, fill=X)


    # --- Utility Functions for Treeview and Tag Management ---

    def add_tag_to_treeviewer(py2html_element_data, treeview_parent_id):
        """Adds a tag's representation to the Treeview.
        
        Args:
            py2html_element_data (dict): The dictionary representing the tag as stored in a py2html.Parent's .tags.
                                         For a Frame/div, its 'content' here should be the py2html.Parent object.
                                         (This is the GUI's internal representation, not what's in py2html.py's .tags for div content).
            treeview_parent_id (str): The ID of the Treeview item that this new item
                                       should be a child of. 
        Returns:
            str: The Treeview item ID of the newly inserted item.
        """
        tag_type = py2html_element_data["type"]
        display_text = ""

        # --- Generate display_text based on tag type ---
        if tag_type == "textnode":
            display_text = f"Text: \"{py2html_element_data['content'][:30]}...\"" if len(py2html_element_data['content']) > 30 else f"Text: \"{py2html_element_data['content']}\""
        elif tag_type in ["button", "p", "textarea"]:
            display_text = f"{tag_type.capitalize()}: \"{py2html_element_data.get('content', '')}\""
        elif tag_type.startswith("h"):
            display_text = f"Heading {tag_type[1]}: \"{py2html_element_data.get('content', '')}\""
        elif tag_type == "img":
            display_text = f"Image: src=\"{py2html_element_data.get('src', '')}\""
        elif tag_type == "a":
            display_text = f"Link: \"{py2html_element_data.get('content', '')}\" (to {py2html_element_data.get('attrs', {}).get('href', '')})"
        elif tag_type == "div":
            # For a div, if its 'content' is a py2html.Parent object (our GUI's internal state)
            if isinstance(py2html_element_data.get('content'), py2html.Parent):
                display_text = f"Frame (Div): {py2html_element_data.get('display', 'block')}"
            else: # If it's a simple div with string content or empty
                display_text = f"Frame (Div): {py2html_element_data.get('display', 'block')} (Empty)"
        elif tag_type == "script":
            display_text = f"Script: src=\"{py2html_element_data.get('src', '')}\"" if py2html_element_data.get('src') else f"Script: inline code ({len(py2html_element_data.get('content', ''))} chars)"
        else: # CustomTag, e.g., 'span', 'article'
            display_text = f"<{tag_type.capitalize()}> Tag: \"{py2html_element_data.get('content', '')[:30]}...\"" if len(py2html_element_data.get('content', '')) > 30 else f"<{tag_type.capitalize()}> Tag: \"{py2html_element_data.get('content', '')}\""


        # --- Apply colors to Treeview items ---
        tags_to_apply = []
        bg_color = py2html_element_data.get("bg") or py2html_element_data.get("style", {}).get("background-color")
        fg_color = py2html_element_data.get("fg") or py2html_element_data.get("style", {}).get("color")

        try:
            if bg_color:
                treeviewer.tag_configure(f"bg_{bg_color}", background=bg_color)
                tags_to_apply.append(f"bg_{bg_color}")
            if fg_color:
                treeviewer.tag_configure(f"fg_{fg_color}", foreground=fg_color)
                tags_to_apply.append(f"fg_{fg_color}")
        except TclError:
            if bg_color:
                treeviewer.tag_configure(f"bg_{bg_color}", background="#fff")
                tags_to_apply.append(f"bg_{bg_color}")
            if fg_color:
                treeviewer.tag_configure(f"fg_{fg_color}", foreground="#000")
                tags_to_apply.append(f"fg_{fg_color}")


        # Insert the item into the Treeview
        new_item_id = treeviewer.insert(treeview_parent_id, END, text=display_text, tags=tuple(tags_to_apply))
        
        # --- Map Treeview Item to its py2html.Parent manager ---
        # If this element is a container (like a div) AND its 'content' is a py2html.Parent object (GUI's view),
        # it means it holds children managed by that Parent object.
        if tag_type == "div" and isinstance(py2html_element_data.get('content'), py2html.Parent):
            parent_object_for_children = py2html_element_data['content']
            treeview_item_to_py2html_parent_map[new_item_id] = parent_object_for_children
            
            # Recursively add the children of this container to the Treeview
            # The children are in parent_object_for_children.tags
            for child_data in parent_object_for_children.tags:
                add_tag_to_treeviewer(child_data, new_item_id)
        else:
            # For non-container elements, or divs with string content, they don't manage children via a Parent object.
            treeview_item_to_py2html_parent_map[new_item_id] = None 

        return new_item_id

    def update_current_parent_on_select(event=None):
        """
        Updates the global current_py2html_target_parent based on Treeview selection.
        """
        global current_py2html_target_parent, current_treeview_parent_id
        
        selected_items = treeviewer.selection()
        if selected_items:
            selected_item_id = selected_items[0]
            
            # Get the py2html.Parent instance associated with this Treeview item.
            # This is the Parent whose 'tags' list should receive new children.
            target_parent_for_children = treeview_item_to_py2html_parent_map.get(selected_item_id)
            
            if target_parent_for_children is not None: 
                current_py2html_target_parent = target_parent_for_children
                current_treeview_parent_id = selected_item_id
                status_bar_label.config(text=f"Inserting into: '{treeviewer.item(selected_item_id, 'text')}'")
            else:
                # If the selected item is not a container (e.g., a button), 
                # new items should be added to its parent.
                # Get the parent of the selected item in the Treeview
                parent_of_selected_item_id = treeviewer.parent(selected_item_id)
                # Find the py2html.Parent object associated with the parent Treeview item
                current_py2html_target_parent = treeview_item_to_py2html_parent_map.get(parent_of_selected_item_id, html)
                current_treeview_parent_id = parent_of_selected_item_id
                parent_text = treeviewer.item(parent_of_selected_item_id, 'text') if parent_of_selected_item_id else "(Root Document)"
                status_bar_label.config(text=f"Inserting into: '{parent_text}'")
        else:
            # No item selected
            current_py2html_target_parent = html
            current_treeview_parent_id = ""
            status_bar_label.config(text="Inserting into: (Root Document)")

    def _clear_treeviewer():
        """Clears all items from the treeviewer."""
        for item in treeviewer.get_children():
            treeviewer.delete(item)
        treeview_item_to_py2html_parent_map.clear()
        treeview_item_to_py2html_parent_map[""] = html # Re-map the root

    def _repopulate_treeview(parent_py2html_obj=None, treeview_parent_id=""):
        """
        Recursively populates the treeview based on the current html object's structure.
        Used after loading a project.
        """
        if parent_py2html_obj is None:
            parent_py2html_obj = html # Start from the main html object

        for tag_data in parent_py2html_obj.tags:
            # The tag_data's 'content' for a div will be a py2html.Parent object here (GUI's in-memory view)
            add_tag_to_treeviewer(tag_data, treeview_parent_id)
            # add_tag_to_treeviewer will handle recursive calls for children if tag_data is a div.


    # --- Common Input Dialog for Basic Elements ---
    def item_menu(tag_friendly_name, py2html_method_name): 
        def done():
            try:
                p_x = int(padx_entry.get()) if padx_entry.get() else 0
                p_y = int(pady_entry.get()) if pady_entry.get() else 0
            except ValueError:
                messagebox.showerror("Input Error", "Padding values must be integers or empty.")
                return

            details = {
                "fg": fg_entry.get(),
                "bg": bg_entry.get(),
                "bd": bd_entry.get(),
                "bdradius": bdradius_entry.get(),
                "text": text_content.get("1.0", "end-1c"),
                "padx": p_x,
                "pady": p_y
            }
            
            py2html_method = getattr(current_py2html_target_parent, py2html_method_name)

            if py2html_method_name == "Frame":
                # Create a NEW py2html.Parent object to manage the content of this Frame.
                # This is the object that the GUI will use to manage children of this frame.
                frame_inner_parent_manager = py2html.Parent()
                
                # Pass this py2html.Parent object as the 'content' argument to py2html.Frame.
                # py2html.Frame will internally extract frame_inner_parent_manager.tags.
                py2html_method(content=frame_inner_parent_manager, **details)
                
                # Get the newly added Frame's tag data from current_py2html_target_parent.tags
                # This tag_data will have 'content' as a LIST (frame_inner_parent_manager.tags).
                new_frame_tag_data = current_py2html_target_parent.tags[-1]
                
                # CRITICAL: For the GUI's internal representation, change the 'content' in this
                # tag_data dict to point to the py2html.Parent object itself.
                # This allows the GUI to correctly associate the Treeview item with the manager.
                new_frame_tag_data['content'] = frame_inner_parent_manager 

                # Add it to the treeview. add_tag_to_treeviewer will correctly
                # map the Frame's treeview item to frame_inner_parent_manager.
                add_tag_to_treeviewer(new_frame_tag_data, current_treeview_parent_id)

                # If there was initial text, add it as a Label (P tag) inside the newly created frame
                initial_text = details.get("text", "").strip()
                if initial_text:
                    # Add to the new Frame's internal parent manager
                    frame_inner_parent_manager.Label(text=initial_text)
                    # Add this new Label to the Treeview as a child of the newly created Frame's Treeview item
                    # The treeview ID for the new frame is the last child of the current_treeview_parent_id
                    new_frame_treeview_item_id = treeviewer.get_children(current_treeview_parent_id)[-1]
                    add_tag_to_treeviewer(frame_inner_parent_manager.tags[-1], new_frame_treeview_item_id)

            else:
                # For other simple tags (Button, Label, Text), just call the method
                py2html_method(**details)
                # Add the newly created element to the treeview
                # For these, the 'content' in the tag data is just a string, so add_tag_to_treeviewer
                # will correctly map its item to None for child management.
                add_tag_to_treeviewer(current_py2html_target_parent.tags[-1], current_treeview_parent_id)
            
            bm.destroy()

        bm = Toplevel(r)
        bm.focus_force()
        bm.title(f"New {tag_friendly_name} - Properties")
        bm.transient(r)
        bm.resizable(0,0)

        bm.bind("<Control-w>", lambda e: bm.destroy())
        bm.bind("<Escape>", lambda e: bm.destroy())
        bm.bind("<Return>", lambda e: done())
        bm.bind("<Control-Return>", lambda e: done())

        for i in range(9): bm.grid_rowconfigure(i, weight=1)
        for i in range(2): bm.grid_columnconfigure(i, weight=1)

        Label(bm, text="Text Color:").grid(column=0, row=0, sticky=E, padx=10, pady=5)
        fg_entry = ttk.Entry(bm)
        fg_entry.grid(column=1, row=0, sticky=W, padx=(0,10), pady=5)
        fg_entry.insert(END, "#000000" if tag_friendly_name != "Button" else "#00a651")

        Label(bm, text="Background Color:").grid(column=0, row=1, sticky=E, padx=10, pady=5)
        bg_entry = ttk.Entry(bm)
        bg_entry.grid(column=1, row=1, sticky=W, padx=(0,10), pady=5)
        bg_entry.insert(END, "#ffffff" if tag_friendly_name != "Button" else "#deffee")

        Label(bm, text="Border:").grid(column=0, row=2, sticky=E, padx=10, pady=5)
        bd_entry = ttk.Entry(bm)
        bd_entry.grid(column=1, row=2, sticky=W, padx=(0,10), pady=5)
        bd_entry.insert(END, "none")

        Label(bm, text="Corner Rounding (Border Radius):").grid(column=0, row=3, sticky=E, padx=10, pady=5)
        bdradius_entry = ttk.Entry(bm)
        bdradius_entry.grid(column=1, row=3, sticky=W, padx=(0,10), pady=5)
        bdradius_entry.insert(END, "0px" if tag_friendly_name != "Button" else "14px")

        Label(bm, text=f"{tag_friendly_name} Text:").grid(column=0, row=4, columnspan=2, pady=(10,0))
        text_content = Text(bm, height=6, width=40, wrap=WORD)
        text_content.grid(column=0, row=5, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        text_content.insert(END, f"Default {tag_friendly_name} Text.")

        Label(bm, text="Padding X (px):").grid(column=0, row=6, sticky=E, padx=10, pady=5)
        padx_entry = ttk.Entry(bm)
        padx_entry.grid(column=1, row=6, sticky=W, padx=(0,10), pady=5)
        padx_entry.insert(END, "5")

        Label(bm, text="Padding Y (px):").grid(column=0, row=7, sticky=E, padx=10, pady=5)
        pady_entry = ttk.Entry(bm)
        pady_entry.grid(column=1, row=7, sticky=W, padx=(0,10), pady=5)
        pady_entry.insert(END, "5")

        done_btn = ttk.Button(bm, text=f"Insert {tag_friendly_name}", command=done, style="Accent.TButton")
        done_btn.grid(column=0, row=8, columnspan=2, pady=(10,10), padx=10, sticky="ew")

    # --- Specific Dialogs for Complex Elements ---

    def heading_menu():
        def done():
            try:
                level = int(level_entry.get())
                if not 1 <= level <= 6:
                    raise ValueError("Heading level must be between 1 and 6.")
                p_x = int(padx_entry.get()) if padx_entry.get() else 0
                p_y = int(pady_entry.get()) if pady_entry.get() else 0
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {e}")
                return

            details = {
                "level": level,
                "text": text_content.get("1.0", "end-1c"),
                "fg": fg_entry.get(),
                "bg": bg_entry.get(),
                "bd": bd_entry.get(),
                "bdradius": bdradius_entry.get(),
                "padx": p_x,
                "pady": p_y
            }
            
            current_py2html_target_parent.Heading(**details)
            add_tag_to_treeviewer(current_py2html_target_parent.tags[-1], current_treeview_parent_id)
            hm.destroy()

        hm = Toplevel(r)
        hm.focus_force()
        hm.title("New Heading - Properties")
        hm.transient(r)
        hm.resizable(0,0)
        hm.bind("<Escape>", lambda e: hm.destroy())

        Label(hm, text="Heading Level (1-6):").grid(row=0, column=0, sticky=E, padx=10, pady=5)
        level_entry = ttk.Entry(hm)
        level_entry.grid(row=0, column=1, sticky=W, padx=(0,10), pady=5)
        level_entry.insert(END, "1")

        Label(hm, text="Text Color:").grid(row=1, column=0, sticky=E, padx=10, pady=5)
        fg_entry = ttk.Entry(hm)
        fg_entry.grid(row=1, column=1, sticky=W, padx=(0,10), pady=5)
        fg_entry.insert(END, "#333")

        Label(hm, text="Background Color:").grid(row=2, column=0, sticky=E, padx=10, pady=5)
        bg_entry = ttk.Entry(hm)
        bg_entry.grid(row=2, column=1, sticky=W, padx=(0,10), pady=5)
        bg_entry.insert(END, "transparent")

        Label(hm, text="Border:").grid(row=3, column=0, sticky=E, padx=10, pady=5)
        bd_entry = ttk.Entry(hm)
        bd_entry.grid(row=3, column=1, sticky=W, padx=(0,10), pady=5)
        bd_entry.insert(END, "none")

        Label(hm, text="Corner Rounding (Border Radius):").grid(row=4, column=0, sticky=E, padx=10, pady=5)
        bdradius_entry = ttk.Entry(hm)
        bdradius_entry.grid(row=4, column=1, sticky=W, padx=(0,10), pady=5)
        bdradius_entry.insert(END, "0px")

        Label(hm, text="Heading Text:").grid(row=5, column=0, columnspan=2, pady=(10,0))
        text_content = Text(hm, height=6, width=40, wrap=WORD)
        text_content.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        text_content.insert(END, "Py2HTML Heading")

        Label(hm, text="Padding X (px):").grid(row=7, column=0, sticky=E, padx=10, pady=5)
        padx_entry = ttk.Entry(hm)
        padx_entry.grid(row=7, column=1, sticky=W, padx=(0,10), pady=5)
        padx_entry.insert(END, "0")

        Label(hm, text="Padding Y (px):").grid(row=8, column=0, sticky=E, padx=10, pady=5)
        pady_entry = ttk.Entry(hm)
        pady_entry.grid(row=8, column=1, sticky=W, padx=(0,10), pady=5)
        pady_entry.insert(END, "0")

        done_btn = ttk.Button(hm, text="Insert Heading", command=done)
        done_btn.grid(row=9, column=0, columnspan=2, pady=(10,10), padx=10, sticky="ew")

    def image_menu():
        def done():
            try:
                w = width_entry.get() if width_entry.get() else "auto"
                h = height_entry.get() if height_entry.get() else "auto"
            except ValueError:
                messagebox.showerror("Input Error", "Width and Height must be valid CSS units (e.g., '100px', '50%').")
                return

            details = {
                "src": src_entry.get(),
                "alt": alt_entry.get(),
                "width": w,
                "height": h,
                "bd": bd_entry.get(),
                "bdradius": bdradius_entry.get()
            }
            current_py2html_target_parent.Image(**details)
            add_tag_to_treeviewer(current_py2html_target_parent.tags[-1], current_treeview_parent_id)
            im.destroy()

        im = Toplevel(r)
        im.focus_force()
        im.title("New Image - Properties")
        im.transient(r)
        im.resizable(0,0)
        im.bind("<Escape>", lambda e: im.destroy())

        Label(im, text="Source (URL/Path):").grid(row=0, column=0, sticky=E, padx=10, pady=5)
        src_entry = ttk.Entry(im)
        src_entry.grid(row=0, column=1, sticky=W, padx=(0,10), pady=5)
        src_entry.insert(END, "https://via.placeholder.com/150")

        Label(im, text="Alt Text:").grid(row=1, column=0, sticky=E, padx=10, pady=5)
        alt_entry = ttk.Entry(im)
        alt_entry.grid(row=1, column=1, sticky=W, padx=(0,10), pady=5)
        alt_entry.insert(END, "Placeholder Image")

        Label(im, text="Width (e.g., 100px, 50%):").grid(row=2, column=0, sticky=E, padx=10, pady=5)
        width_entry = ttk.Entry(im)
        width_entry.grid(row=2, column=1, sticky=W, padx=(0,10), pady=5)
        width_entry.insert(END, "auto")

        Label(im, text="Height (e.g., 100px, 50%):").grid(row=3, column=0, sticky=E, padx=10, pady=5)
        height_entry = ttk.Entry(im)
        height_entry.grid(row=3, column=1, sticky=W, padx=(0,10), pady=5)
        height_entry.insert(END, "auto")
        
        Label(im, text="Border:").grid(row=4, column=0, sticky=E, padx=10, pady=5)
        bd_entry = ttk.Entry(im)
        bd_entry.grid(row=4, column=1, sticky=W, padx=(0,10), pady=5)
        bd_entry.insert(END, "none")

        Label(im, text="Corner Rounding (Border Radius):").grid(row=5, column=0, sticky=E, padx=10, pady=5)
        bdradius_entry = ttk.Entry(im)
        bdradius_entry.grid(row=5, column=1, sticky=W, padx=(0,10), pady=5)
        bdradius_entry.insert(END, "0px")

        done_btn = ttk.Button(im, text="Insert Image", command=done)
        done_btn.grid(row=6, column=0, columnspan=2, pady=(10,10), padx=10, sticky="ew")

    def link_menu():
        def done():
            try:
                p_x = int(padx_entry.get()) if padx_entry.get() else 0
                p_y = int(pady_entry.get()) if pady_entry.get() else 0
            except ValueError:
                messagebox.showerror("Input Error", "Padding values must be integers or empty.")
                return

            details = {
                "href": href_entry.get(),
                "text": text_content.get("1.0", "end-1c"),
                "fg": fg_entry.get(),
                "bg": bg_entry.get(),
                "bd": bd_entry.get(),
                "bdradius": bdradius_entry.get(),
                "padx": p_x,
                "pady": p_y,
                "text_decor": text_decor_entry.get()
            }
            current_py2html_target_parent.Link(**details)
            add_tag_to_treeviewer(current_py2html_target_parent.tags[-1], current_treeview_parent_id)
            lm.destroy()

        lm = Toplevel(r)
        lm.focus_force()
        lm.title("New Link - Properties")
        lm.transient(r)
        lm.resizable(0,0)
        lm.bind("<Escape>", lambda e: lm.destroy())

        Label(lm, text="Href (URL):").grid(row=0, column=0, sticky=E, padx=10, pady=5)
        href_entry = ttk.Entry(lm)
        href_entry.grid(row=0, column=1, sticky=W, padx=(0,10), pady=5)
        href_entry.insert(END, "https://example.com")

        Label(lm, text="Link Text:").grid(row=1, column=0, columnspan=2, pady=(10,0))
        text_content = Text(lm, height=6, width=40, wrap=WORD)
        text_content.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        text_content.insert(END, "Click Here")

        Label(lm, text="Text Color:").grid(row=3, column=0, sticky=E, padx=10, pady=5)
        fg_entry = ttk.Entry(lm)
        fg_entry.grid(row=3, column=1, sticky=W, padx=(0,10), pady=5)
        fg_entry.insert(END, "#00a651")

        Label(lm, text="Background Color:").grid(row=4, column=0, sticky=E, padx=10, pady=5)
        bg_entry = ttk.Entry(lm)
        bg_entry.grid(row=4, column=1, sticky=W, padx=(0,10), pady=5)
        bg_entry.insert(END, "transparent")

        Label(lm, text="Border:").grid(row=5, column=0, sticky=E, padx=10, pady=5)
        bd_entry = ttk.Entry(lm)
        bd_entry.grid(row=5, column=1, sticky=W, padx=(0,10), pady=5)
        bd_entry.insert(END, "none")

        Label(lm, text="Corner Rounding (Border Radius):").grid(row=6, column=0, sticky=E, padx=10, pady=5)
        bdradius_entry = ttk.Entry(lm)
        bdradius_entry.grid(row=6, column=1, sticky=W, padx=(0,10), pady=5)
        bdradius_entry.insert(END, "0px")

        Label(lm, text="Padding X (px):").grid(row=7, column=0, sticky=E, padx=10, pady=5)
        padx_entry = ttk.Entry(lm)
        padx_entry.grid(row=7, column=1, sticky=W, padx=(0,10), pady=5)
        padx_entry.insert(END, "0")

        Label(lm, text="Padding Y (px):").grid(row=8, column=0, sticky=E, padx=10, pady=5)
        pady_entry = ttk.Entry(lm)
        pady_entry.grid(row=8, column=1, sticky=W, padx=(0,10), pady=5)
        pady_entry.insert(END, "0")

        Label(lm, text="Text Decoration:").grid(row=9, column=0, sticky=E, padx=10, pady=5)
        text_decor_entry = ttk.Combobox(lm, values=["underline", "none", "overline", "line-through"])
        text_decor_entry.grid(row=9, column=1, sticky=W, padx=(0,10), pady=5)
        text_decor_entry.set("underline")

        done_btn = ttk.Button(lm, text="Insert Link", command=done)
        done_btn.grid(row=10, column=0, columnspan=2, pady=(10,10), padx=10, sticky="ew")

    def frame_menu():
        def done():
            try:
                p_x = int(padx_entry.get()) if padx_entry.get() else 0
                p_y = int(pady_entry.get()) if pady_entry.get() else 0
                m_x = marginx_entry.get() 
                m_y = marginy_entry.get()
            except ValueError:
                messagebox.showerror("Input Error", "Padding values must be integers. Margin values must be valid CSS units.")
                return

            flex_config = {
                "align-items": align_items_var.get(),
                "justify-content": justify_content_var.get(),
                "flex-direction": flex_direction_var.get(),
                "flex-wrap": flex_wrap_var.get(),
                "gap": gap_entry.get()
            }
            offset_config = {
                "top": offset_top_entry.get(),
                "left": offset_left_entry.get(),
                "right": offset_right_entry.get(),
                "bottom": offset_bottom_entry.get(),
            }

            details = {
                "fg": fg_entry.get(),
                "bg": bg_entry.get(),
                "bd": bd_entry.get(),
                "bdradius": bdradius_entry.get(),
                "padx": p_x,
                "pady": p_y,
                "width": width_entry.get(),
                "height": height_entry.get(),
                "marginx": m_x,
                "marginy": m_y,
                "content_manager": display_var.get(), # Renamed 'display' to 'content_manager' to avoid conflict with py2html.py's internal 'display'
                "flex_config": flex_config if display_var.get() == "flex" else {},
                "position": position_var.get(),
                "offset": offset_config
            }

            # Create a NEW py2html.Parent object to manage the content of this Frame.
            # This is the object that the GUI will use to manage children of this frame.
            frame_inner_parent_manager = py2html.Parent()
            
            # Pass this py2html.Parent object as the 'content' argument to py2html.Frame.
            # py2html.Frame will internally extract frame_inner_parent_manager.tags and put that LIST
            # into the tag dictionary that gets appended to current_py2html_target_parent.tags.
            current_py2html_target_parent.Frame(content=frame_inner_parent_manager, **details)
            
            # Get the newly added Frame's tag data from current_py2html_target_parent.tags
            # This tag_data will have 'content' as a LIST (frame_inner_parent_manager.tags).
            new_frame_tag_data = current_py2html_target_parent.tags[-1]
            
            # CRITICAL: For the GUI's internal representation, change the 'content' in this
            # tag_data dict to point to the py2html.Parent object itself.
            # This allows the GUI to correctly associate the Treeview item with the manager.
            new_frame_tag_data['content'] = frame_inner_parent_manager 

            # Add it to the treeview. add_tag_to_treeviewer will correctly
            # map the Frame's treeview item to frame_inner_parent_manager.
            add_tag_to_treeviewer(new_frame_tag_data, current_treeview_parent_id)
            
            # If there was initial text, add it as a Label (P tag) inside the newly created frame
            initial_text = content_text.get("1.0", "end-1c").strip()
            if initial_text:
                # Add to the new Frame's internal parent manager
                frame_inner_parent_manager.Label(text=initial_text)
                # Add this new Label to the Treeview as a child of the newly created Frame's Treeview item
                # The treeview ID for the new frame is the last child of the current_treeview_parent_id
                new_frame_treeview_item_id = treeviewer.get_children(current_treeview_parent_id)[-1]
                add_tag_to_treeviewer(frame_inner_parent_manager.tags[-1], new_frame_treeview_item_id)

            fm.destroy()

        fm = Toplevel(r)
        fm.focus_force()
        fm.title("New Frame (Div) - Properties")
        fm.transient(r)
        fm.grab_set()
        fm.resizable(0,0)
        fm.bind("<Escape>", lambda e: fm.destroy())

        # Create a notebook for tabs
        notebook = ttk.Notebook(fm)
        notebook.pack(expand=1, fill="both", padx=10, pady=10)

        # --- General Tab ---
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")

        Label(general_frame, text="Text Color:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
        fg_entry = ttk.Entry(general_frame)
        fg_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        fg_entry.insert(END, "#000")

        Label(general_frame, text="Background Color:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        bg_entry = ttk.Entry(general_frame)
        bg_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        bg_entry.insert(END, "#fff")

        Label(general_frame, text="Border:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
        bd_entry = ttk.Entry(general_frame)
        bd_entry.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        bd_entry.insert(END, "none")

        Label(general_frame, text="Border Radius:").grid(row=3, column=0, sticky=E, padx=5, pady=5)
        bdradius_entry = ttk.Entry(general_frame)
        bdradius_entry.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        bdradius_entry.insert(END, "0px")
        
        Label(general_frame, text="Initial Content Text (optional Label tag inside):").grid(row=4, column=0, columnspan=2, pady=(10,0))
        content_text = Text(general_frame, height=3, width=40, wrap=WORD)
        content_text.grid(row=5, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="ew")
        content_text.insert(END, "") 

        Label(general_frame, text="Padding X (px):").grid(row=6, column=0, sticky=E, padx=5, pady=5)
        padx_entry = ttk.Entry(general_frame)
        padx_entry.grid(row=6, column=1, sticky=W, padx=5, pady=5)
        padx_entry.insert(END, "15")

        Label(general_frame, text="Padding Y (px):").grid(row=7, column=0, sticky=E, padx=5, pady=5)
        pady_entry = ttk.Entry(general_frame)
        pady_entry.grid(row=7, column=1, sticky=W, padx=5, pady=5)
        pady_entry.insert(END, "15")

        Label(general_frame, text="Width:").grid(row=8, column=0, sticky=E, padx=5, pady=5)
        width_entry = ttk.Entry(general_frame)
        width_entry.grid(row=8, column=1, sticky=W, padx=5, pady=5)
        width_entry.insert(END, "auto")

        Label(general_frame, text="Height:").grid(row=9, column=0, sticky=E, padx=5, pady=5)
        height_entry = ttk.Entry(general_frame)
        height_entry.grid(row=9, column=1, sticky=W, padx=5, pady=5)
        height_entry.insert(END, "auto")

        Label(general_frame, text="Margin X (e.g., 10px, auto):").grid(row=10, column=0, sticky=E, padx=5, pady=5)
        marginx_entry = ttk.Entry(general_frame)
        marginx_entry.grid(row=10, column=1, sticky=W, padx=5, pady=5)
        marginx_entry.insert(END, "0")

        Label(general_frame, text="Margin Y (e.g., 10px, auto):").grid(row=11, column=0, sticky=E, padx=5, pady=5)
        marginy_entry = ttk.Entry(general_frame)
        marginy_entry.grid(row=11, column=1, sticky=W, padx=5, pady=5)
        marginy_entry.insert(END, "0")

        # --- Layout Tab ---
        layout = ttk.Frame(notebook)
        notebook.add(layout, text="Layout")

        position_frame = ttk.LabelFrame(layout, text="Positon")
        position_frame.pack(fill=BOTH, expand=1)

        Label(position_frame, text="Position Type:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
        position_var = StringVar()
        position_options = ["static", "relative", "absolute", "fixed", "sticky"]
        position_menu = ttk.Combobox(position_frame, textvariable=position_var, values=position_options, state="readonly")
        position_menu.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        position_menu.set("static")

        Label(position_frame, text="Top:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        offset_top_entry = ttk.Entry(position_frame)
        offset_top_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        offset_top_entry.insert(END, "")

        Label(position_frame, text="Left:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
        offset_left_entry = ttk.Entry(position_frame)
        offset_left_entry.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        offset_left_entry.insert(END, "")

        Label(position_frame, text="Right:").grid(row=3, column=0, sticky=E, padx=5, pady=5)
        offset_right_entry = ttk.Entry(position_frame)
        offset_right_entry.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        offset_right_entry.insert(END, "")

        Label(position_frame, text="Bottom:").grid(row=4, column=0, sticky=E, padx=5, pady=5)
        offset_bottom_entry = ttk.Entry(position_frame)
        offset_bottom_entry.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        offset_bottom_entry.insert(END, "")


        # --- Flexbox Tab ---
        flex_frame = ttk.LabelFrame(layout, text="Display")
        flex_frame.pack(fill=BOTH, expand=1)

        Label(flex_frame, text="Display:").grid(row=12, column=0, sticky=E, padx=5, pady=5)
        display_var = StringVar()
        display_options = ["block", "inline", "inline-block", "flex", "none"]
        display_menu = ttk.Combobox(flex_frame, textvariable=display_var, values=display_options, state="readonly")
        display_menu.grid(row=12, column=1, sticky=W, padx=5, pady=5)
        display_menu.set("block")



        Label(flex_frame, text="Align Items:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
        align_items_var = StringVar()
        align_items_options = ["stretch", "flex-start", "flex-end", "center", "baseline"]
        align_items_menu = ttk.Combobox(flex_frame, textvariable=align_items_var, values=align_items_options, state="readonly")
        align_items_menu.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        align_items_menu.set("stretch")

        Label(flex_frame, text="Justify Content:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
        justify_content_var = StringVar()
        justify_content_options = ["flex-start", "flex-end", "center", "space-between", "space-around", "space-evenly"]
        justify_content_menu = ttk.Combobox(flex_frame, textvariable=justify_content_var, values=justify_content_options, state="readonly")
        justify_content_menu.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        justify_content_menu.set("flex-start")

        Label(flex_frame, text="Flex Direction:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
        flex_direction_var = StringVar()
        flex_direction_options = ["row", "row-reverse", "column", "column-reverse"]
        flex_direction_menu = ttk.Combobox(flex_frame, textvariable=flex_direction_var, values=flex_direction_options, state="readonly")
        flex_direction_menu.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        flex_direction_menu.set("row")

        Label(flex_frame, text="Flex Wrap:").grid(row=3, column=0, sticky=E, padx=5, pady=5)
        flex_wrap_var = StringVar()
        flex_wrap_options = ["nowrap", "wrap", "wrap-reverse"]
        flex_wrap_menu = ttk.Combobox(flex_frame, textvariable=flex_wrap_var, values=flex_wrap_options, state="readonly")
        flex_wrap_menu.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        flex_wrap_menu.set("nowrap")

        Label(flex_frame, text="Gap (e.g., 10px, 1em):").grid(row=4, column=0, sticky=E, padx=5, pady=5)
        gap_entry = ttk.Entry(flex_frame)
        gap_entry.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        gap_entry.insert(END, "0")

        # --- Done Button for Frame Dialog ---
        done_btn = ttk.Button(fm, text="Insert Frame", command=done)
        done_btn.pack(pady=(10,10), padx=10, fill="x")

    def custom_tag_menu():
        def done():
            try:
                p_x = int(padx_entry.get()) if padx_entry.get() else 0
                p_y = int(pady_entry.get()) if pady_entry.get() else 0
            except ValueError:
                messagebox.showerror("Input Error", "Padding values must be integers or empty.")
                return

            details = {
                "tag": tag_name_entry.get(),
                "content": text_content.get("1.0", "end-11c"), # This would make it a non-container
                "fg": fg_entry.get(),
                "bg": bg_entry.get(),
                "bd": bd_entry.get(),
                "bdradius": bdradius_entry.get(),
                "padx": p_x,
                "pady": p_y
            }
            # The CustomTag method in py2html should handle if 'content' is a string
            current_py2html_target_parent.CustomTag(**details) 
            add_tag_to_treeviewer(current_py2html_target_parent.tags[-1], current_treeview_parent_id)
            ctm.destroy()

        ctm = Toplevel(r)
        ctm.focus_force()
        ctm.title("New Custom Tag - Properties")
        ctm.transient(r)
        ctm.resizable(0,0)
        ctm.bind("<Escape>", lambda e: ctm.destroy())

        Label(ctm, text="Tag Name (e.g., span, article):").grid(row=0, column=0, sticky=E, padx=10, pady=5)
        tag_name_entry = ttk.Entry(ctm)
        tag_name_entry.grid(row=0, column=1, sticky=W, padx=(0,10), pady=5)
        tag_name_entry.insert(END, "span")

        Label(ctm, text="Text Color:").grid(row=1, column=0, sticky=E, padx=10, pady=5)
        fg_entry = ttk.Entry(ctm)
        fg_entry.grid(row=1, column=1, sticky=W, padx=(0,10), pady=5)
        fg_entry.insert(END, "#000")

        Label(ctm, text="Background Color:").grid(row=2, column=0, sticky=E, padx=10, pady=5)
        bg_entry = ttk.Entry(ctm)
        bg_entry.grid(row=2, column=1, sticky=W, padx=(0,10), pady=5)
        bg_entry.insert(END, "transparent")

        Label(ctm, text="Border:").grid(row=3, column=0, sticky=E, padx=10, pady=5)
        bd_entry = ttk.Entry(ctm)
        bd_entry.grid(row=3, column=1, sticky=W, padx=(0,10), pady=5)
        bd_entry.insert(END, "none")

        Label(ctm, text="Corner Rounding (Border Radius):").grid(row=4, column=0, sticky=E, padx=10, pady=5)
        bdradius_entry = ttk.Entry(ctm)
        bdradius_entry.grid(row=4, column=1, sticky=W, padx=(0,10), pady=5)
        bdradius_entry.insert(END, "0px")

        Label(ctm, text="Content:").grid(row=5, column=0, columnspan=2, pady=(10,0))
        text_content = Text(ctm, height=6, width=40, wrap=WORD)
        text_content.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        text_content.insert(END, "Custom tag content")

        Label(ctm, text="Padding X (px):").grid(row=7, column=0, sticky=E, padx=10, pady=5)
        padx_entry = ttk.Entry(ctm)
        padx_entry.grid(row=7, column=1, sticky=W, padx=(0,10), pady=5)
        padx_entry.insert(END, "0")

        Label(ctm, text="Padding Y (px):").grid(row=8, column=0, sticky=E, padx=10, pady=5)
        pady_entry = ttk.Entry(ctm)
        pady_entry.grid(row=8, column=1, sticky=W, padx=(0,10), pady=5)
        pady_entry.insert(END, "0")

        done_btn = ttk.Button(ctm, text="Insert Custom Tag", command=done)
        done_btn.grid(row=9, column=0, columnspan=2, pady=(10,10), padx=10, sticky="ew")

    def script_menu():
        def done():
            src = src_entry.get().strip()
            inline_code = script_content.get("1.0", "end-1c").strip()

            if not src and not inline_code:
                messagebox.showerror("Input Error", "Please provide either a Source URL or Inline Code for the script.")
                return
            if src and inline_code:
                messagebox.showwarning("Warning", "It's generally not recommended to have both src and inline code in a script tag. Only src will be used.")

            details = {}
            if src:
                details["src"] = src
            elif inline_code:
                details["code"] = inline_code # Pass as 'code' for py2html.Script
            
            current_py2html_target_parent.Script(**details)
            add_tag_to_treeviewer(current_py2html_target_parent.tags[-1], current_treeview_parent_id)
            sm.destroy()

        sm = Toplevel(r)
        sm.focus_force()
        sm.title("New Script Tag - Properties")
        sm.transient(r)
        sm.resizable(0,0)
        sm.bind("<Escape>", lambda e: sm.destroy())

        Label(sm, text="Source (URL, optional):").grid(row=0, column=0, sticky=E, padx=10, pady=5)
        src_entry = ttk.Entry(sm)
        src_entry.grid(row=0, column=1, sticky=W, padx=(0,10), pady=5)
        src_entry.insert(END, "")

        Label(sm, text="Inline JavaScript Code (optional):").grid(row=1, column=0, columnspan=2, pady=(10,0))
        script_content = Text(sm, height=10, width=50, wrap=WORD)
        script_content.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        script_content.insert(END, "alert('Hello from Py2HTML!');")

        done_btn = ttk.Button(sm, text="Insert Script", command=done)
        done_btn.grid(row=3, column=0, columnspan=2, pady=(10,10), padx=10, sticky="ew")
    
    treeviewer.bind("<<TreeviewSelect>>", update_current_parent_on_select)
    style = ttk.Style(r)
    style.configure('Treeview', rowheight=40, rowwidth=100)



    # --- Menu Bar ---
    menubar = Menu(r)
    r.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Project", command=lambda: [newwindow(), _clear_treeviewer()])
    file_menu.add_command(label="Open Project (JSON)", command=lambda: openjson_project())
    file_menu.add_command(label="Save Project (JSON)", command=lambda: savejson_project())
    file_menu.add_separator()
    file_menu.add_command(label="Export HTML", command=lambda: export_html())
    file_menu.add_command(label="Exit", command=r.quit)

    insert_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Insert", menu=insert_menu)
    insert_menu.add_command(label="Button", command=lambda: item_menu("Button", "Button"))
    insert_menu.add_command(label="Label (Paragraph)", command=lambda: item_menu("Label", "Label"))
    insert_menu.add_command(label="Heading", command=lambda: heading_menu())
    insert_menu.add_command(label="Image", command=lambda: image_menu())
    insert_menu.add_command(label="Link", command=lambda: link_menu())
    insert_menu.add_command(label="Textarea", command=lambda: item_menu("Textarea", "Text"))
    insert_menu.add_command(label="Frame (Div)", command=lambda: frame_menu())
    insert_menu.add_command(label="Custom Tag", command=lambda: custom_tag_menu())
    insert_menu.add_command(label="Script", command=lambda: script_menu())

    preview_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="HTML", menu=preview_menu)
    preview_menu.add_command(label="Show Preview", accelerator="Ctrl+Enter", command=lambda: create_window())
    preview_menu.add_command(label="Get HTML", accelerator="Ctrl+P", command=lambda: get_html())


    r.bind("<Control-Return>", lambda _: create_window())
    r.bind("<Control-p>", lambda _: get_html())

    def create_window():
        webview.create_window("Py2HTML Preview", html=html.getHTML())
        webview.start()






    # --- HTML Preview Frame ---
    # preview_frame = Frame(r, bd=2, relief="groove")
    # preview_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        
    def get_html():
        prwin = Tk()
        mb = ttk.Menubutton(prwin, text="Options")
        mb.pack()
        opm = Menu(mb, tearoff=0)
        mb["menu"] = opm
        frmt = BooleanVar()
        opm.add_checkbutton(label="Format", variable=frmt)
        Label(prwin, text="HTML Preview").pack(side=TOP, pady=5)
        # _format = ttk.Checkbutton(prwin, text="Format")
        # _format.pack(side=BOTTOM)

        prtext = Text(prwin, bd=5, relief=GROOVE)
        prtext.pack(side=LEFT, fill=BOTH, expand=1)

        webview = HtmlFrame(prwin,)
        webview.pack(fill="both", expand=1, side=RIGHT)

        
        def show_preview():
            generated_html = html.getHTML(format=1)
            webview.load_html(generated_html)
            prtext.delete(1.0, END)
            prtext.insert("end-1c", generated_html)
            prwin.after(2000, show_preview) # Refresh every 2 seconds
        
        show_preview()

    # --- Project Save/Load Functions ---

    def savejson_project():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            # Prepare the html.tags for JSON serialization.
            # This means replacing py2html.Parent objects in 'content' of divs with their actual tags lists.
            def _prepare_for_json(tags_list):
                json_ready_list = []
                for tag_data in tags_list:
                    copied_tag = copy.deepcopy(tag_data)
                    # If a div's content is a Parent object (GUI's internal representation),
                    # replace it with its .tags list for JSON saving.
                    if copied_tag.get('type') == 'div' and isinstance(copied_tag.get('content'), py2html.Parent):
                        copied_tag['content'] = _prepare_for_json(copied_tag['content'].tags)
                    json_ready_list.append(copied_tag)
                return json_ready_list

            json_data_to_save = _prepare_for_json(html.tags)

            with open(filepath, 'w') as f:
                json.dump(json_data_to_save, f, indent=4)
            messagebox.showinfo("Save Project", "Project saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save project: {e}")

    def openjson_project():
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r') as f:
                loaded_json_tags = json.load(f)
            
            _clear_treeviewer() 

            global html, current_py2html_target_parent, current_treeview_parent_id
            
            # Reconstruct the py2html.Parent objects in memory.
            # This function will return the top-level list of reconstructed tag dictionaries,
            # where 'div' content points to py2html.Parent objects for GUI management.
            reconstructed_top_level_tags = _recursively_reconstruct_py2html_objects(loaded_json_tags)
            
            # Now, assign this reconstructed list to our main 'html' Parent object's tags.
            html.tags = reconstructed_top_level_tags 
            
            # Reset the current target to the root HTML object
            current_py2html_target_parent = html
            current_treeview_parent_id = ""
            treeview_item_to_py2html_parent_map[""] = html 

            # Repopulate the treeview using the reconstructed html object
            _repopulate_treeview() 
            
            messagebox.showinfo("Open Project", "Project opened successfully!")
        except json.JSONDecodeError as e:
            messagebox.showerror("Load Error", f"Failed to load project: Invalid JSON file.\\n{e}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load project: {e}")

    def export_html():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if not filepath:
            return
        try:
            with open(filepath, 'w') as f:
                # py2html.getHTML() directly generates HTML from the current state,
                # which should already have Parent objects if loaded/created correctly.
                f.write(html.getHTML(format=True)) 
            messagebox.showinfo("Export HTML", "HTML exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export HTML: {e}")

    def delete_selected_element():
        global current_py2html_target_parent, current_treeview_parent_id
        selected_items = treeviewer.selection()
        if not selected_items:
            messagebox.showinfo("Delete Element", "Please select an element to delete.")
            return

        selected_item_id = selected_items[0]
        parent_treeview_id = treeviewer.parent(selected_item_id)
        
        # Get the py2html.Parent object that manages the *children* of the parent Treeview item
        # If parent_treeview_id is "", then it's the root HTML object.
        parent_py2html_obj = treeview_item_to_py2html_parent_map.get(parent_treeview_id, html)
        
        # Get the index of the selected item within its parent's children (tags list)
        item_index_to_delete = -1
        # The treeview item ID doesn't directly map to the list index,
        # so we need to find it by comparing its content or other properties.
        # This is a bit brittle, a unique ID per tag would be better for robust deletion.
        # For now, let's rely on iterating and matching by display text.
        
        item_text_in_treeview = treeviewer.item(selected_item_id, 'text')
        
        # Iterate through the parent_py2html_obj's tags to find the matching item.
        for i, tag_dict in enumerate(parent_py2html_obj.tags):
            display_text_for_comparison = ""
            tag_type = tag_dict.get("type", "")

            # Re-generate the display text based on tag_dict for comparison
            if tag_type == "textnode":
                display_text_for_comparison = f"Text: \"{tag_dict['content'][:30]}...\"" if len(tag_dict['content']) > 30 else f"Text: \"{tag_dict['content']}\""
            elif tag_type in ["button", "p", "textarea"]:
                display_text_for_comparison = f"{tag_type.capitalize()}: \"{tag_dict.get('content', '')}\""
            elif tag_type.startswith("h"):
                display_text_for_comparison = f"Heading {tag_type[1]}: \"{tag_dict.get('content', '')}\""
            elif tag_type == "img":
                display_text_for_comparison = f"Image: src=\"{tag_dict.get('src', '')}\""
            elif tag_type == "a":
                display_text_for_comparison = f"Link: \"{tag_dict.get('content', '')}\" (to {tag_dict.get('attrs', {}).get('href', '')})"
            elif tag_type == "div":
                # For a div, need to check if its 'content' is a Parent object (GUI view)
                if isinstance(tag_dict.get('content'), py2html.Parent):
                    display_text_for_comparison = f"Frame (Div): {tag_dict.get('display', 'block')}"
                else:
                    display_text_for_comparison = f"Frame (Div): {tag_dict.get('display', 'block')} (Empty)"
            elif tag_type == "script":
                display_text_for_comparison = f"Script: src=\"{tag_dict.get('src', '')}\"" if tag_dict.get('src') else f"Script: inline code ({len(tag_dict.get('content', ''))} chars)"
            else: # CustomTag
                display_text_for_comparison = f"<{tag_type.capitalize()}> Tag: \"{tag_dict.get('content', '')[:30]}...\"" if len(tag_dict.get('content', '')) > 30 else f"<{tag_type.capitalize()}> Tag: \"{tag_dict.get('content', '')}\""

            if display_text_for_comparison == item_text_in_treeview:
                item_index_to_delete = i
                break
        
        if item_index_to_delete != -1:
            del parent_py2html_obj.tags[item_index_to_delete]
            treeviewer.delete(selected_item_id)
            # Remove from map as well
            if selected_item_id in treeview_item_to_py2html_parent_map:
                del treeview_item_to_py2html_parent_map[selected_item_id]
            messagebox.showinfo("Delete Element", f"Element '{item_text_in_treeview}' deleted.")
            # After deletion, update the current target parent in case the deleted item
            # was the current target or its child.
            update_current_parent_on_select() 
        else:
            messagebox.showwarning("Delete Error", "Could not find the corresponding element in the data model. Treeview might be out of sync. Please try saving and reloading the project.")
            

    # --- Setup the GUI Layout ---
    button_frame = Frame(r)
    # ttk.Button(button_frame, text="Insert Button", command=lambda: item_menu("Button", "Button")).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    # ttk.Button(button_frame, text="Insert Label", command=lambda: item_menu("Label", "Label")).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    # ttk.Button(button_frame, text="Insert Heading", command=lambda: heading_menu()).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    # ttk.Button(button_frame, text="Insert Image", command=lambda: image_menu()).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    # ttk.Button(button_frame, text="Insert Link", command=lambda: link_menu()).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    # ttk.Button(button_frame, text="Insert Textarea", command=lambda: item_menu("Textarea", "Textarea")).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    ttk.Button(button_frame, text="Insert Frame (Div)", command=lambda: frame_menu()).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    ttk.Button(button_frame, text="Custom Tag", command=lambda: custom_tag_menu()).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    ttk.Button(button_frame, text="Custom Scripts", command=lambda: script_menu()).pack(side=TOP, padx=2, pady=2, fill=BOTH, expand=1)
    ttk.Button(r, text="Delete Selected", command=delete_selected_element, style="Accent.TButton").pack(side=BOTTOM, padx=2, fill=X, expand=1, anchor=S, pady=(0, 10))

    button_frame.pack(side=TOP, fill=X, pady=5)

    s = ttk.Style()
    s.configure("Del.TButton", background="#f7d2d2", foreground="#ff0000", font=("Arial", 10, "bold"), hoverbackground="#f7d2d2")
    s.configure("TLabelFrame", padx=10)
    sv_ttk.set_theme("light")

    font.nametofont("SunValleyCaptionFont").configure(size=10)
    font.nametofont("SunValleyBodyStrongFont").configure(size=18)
    font.nametofont("SunValleyBodyLargeFont").configure(size=10)
    font.nametofont("SunValleySubtitleFont").configure(size=22)
    font.nametofont("SunValleyTitleFont").configure(size=18)
    font.nametofont("SunValleyTitleLargeFont").configure(size=42)
    font.nametofont("SunValleyDisplayFont").configure(size=72)

    font.nametofont("SunValleyBodyFont").configure(size=10, family="segoe ui")


    # Start the preview refresh loop

    r.mainloop()

# --- Initial Window Call ---
if __name__ == "__main__":
    try:
        import py2html
    except ImportError:
        messagebox.showerror("Error", "Could not find 'py2html.py'. Please ensure it is in the same directory.")
        exit()
    newwindow()

''')
    
def win():
    global p
    p = Toplevel(r)
    p.title("Py2Html Installer")
    p.transient(r)
    pr = ttk.Progressbar(p, length=600, mode="indeterminate")
    pr.start(10)
    pr.pack(pady=20, padx=20, fill=X)
    p.mainloop()

r = Tk()
r.title("Py2html Installer")
r.geometry("600x600")
r.transient()
r.resizable(False, False)

Label(r, text="Py2html Installer", font=("Arial", 26)).pack(pady=10)
Label(r, text="This will install py2html and its dependencies. Click 'Install' to proceed.").pack(pady=10, fill=X)
cv = BooleanVar()
Checkbutton(r, text="Install Py2Html GUI", variable=cv).pack()
Button(r, text="Install", command=lambda: threading.Thread(target=lambda: [win(), install_py2html(cv.get)]).start()).pack(pady=20)
r.mainloop()
