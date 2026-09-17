#!/usr/bin/env python3
"""Layout check for the module's decks - run after every deck edit.

Renders each deck in headless Chrome at 1280x720 and reports, per slide:
  body     the slide body is taller than the space it has (content runs into the footer)
  scrolls  the body or a card needs a scrollbar at the fitted zoom (readable, but should not happen)
  top/bottom/edge  a block sits over the title, the footer, or past the right margin
  pre      a code block is clipped on the right (pre is overflow:hidden)
  svgtext  SVG text runs outside its own viewBox

    python3 check-decks.py                              # every deck in ../python-accelerated
    python3 check-decks.py ../presentation/t3-service.html

Exit status is the number of problems, so it can gate a commit.
"""
import glob
import html
import json
import os
import re
import subprocess
import sys

PROBE = r"""
(function(){
  var out=[], slides=[].slice.call(document.querySelectorAll('.slide'));
  document.getElementById('stage').style.transform='none';   // measure at authored 1280x720
  slides.forEach(function(s){ s.classList.remove('active'); });
  slides.forEach(function(sl, i){
    sl.classList.add('active');
    if (window.__fitSlide) window.__fitSlide(sl);   // measure what the audience sees
    // a grid slide grows rather than scrolls, so compare against its fixed frame
    var box=sl.getBoundingClientRect();
    var foot=sl.querySelector(':scope > footer');
    var tall=Math.max(sl.scrollHeight-sl.clientHeight, foot ? foot.getBoundingClientRect().bottom-box.bottom : 0);
    if(tall > 2) out.push({s:i+1,k:'body',d:Math.round(tall)});
    if(sl.scrollWidth > sl.clientWidth + 2) out.push({s:i+1,k:'wide',d:sl.scrollWidth-sl.clientWidth});
    var head=sl.querySelector(':scope > header'), edge=head ? head.getBoundingClientRect().right : box.right;
    var top=head ? head.getBoundingClientRect().bottom : box.top, bottom=foot ? foot.getBoundingClientRect().top : box.bottom;
    sl.querySelectorAll(':scope > .body > *, :scope > .body .card, :scope > .body table, :scope > .body pre, :scope > .body svg').forEach(function(el){
      var r=el.getBoundingClientRect(), t=(el.textContent||'').trim().slice(0,40);
      if(r.right-edge > 2) out.push({s:i+1,k:'edge',d:Math.round(r.right-edge),t:t});
      if(top-r.top > 2) out.push({s:i+1,k:'top',d:Math.round(top-r.top),t:t});
      if(r.bottom-bottom > 2) out.push({s:i+1,k:'bottom',d:Math.round(r.bottom-bottom),t:t});
    });
    // footer text truncated by its ellipsis - shorten the deck's data-deck label
    if(foot) foot.querySelectorAll(':scope > span').forEach(function(sp){
      if(sp.scrollWidth > sp.clientWidth + 1)
        out.push({s:i+1,k:'footer',d:sp.scrollWidth-sp.clientWidth,t:sp.textContent.trim().slice(0,40)});
    });
    sl.querySelectorAll(':scope > .body').forEach(function(el){
      var over=Math.max(el.scrollHeight-el.clientHeight, el.scrollWidth-el.clientWidth);
      if(over > 2) out.push({s:i+1,k:'scrolls',d:Math.round(over),t:(el.textContent||'').trim().slice(0,40)});
    });
    sl.querySelectorAll('pre').forEach(function(p){
      var over=Math.max(p.scrollWidth-p.clientWidth, p.getBoundingClientRect().right-(box.right-30));
      if(over > 2) out.push({s:i+1,k:'pre',d:Math.round(over),t:p.textContent.trim().slice(0,40)});
    });
    sl.querySelectorAll('svg[viewBox]').forEach(function(svg){
      var vb=svg.getAttribute('viewBox').trim().split(/[\s,]+/).map(Number);
      svg.querySelectorAll('text').forEach(function(t){
        if(t.getAttribute('transform')) return;
        var b; try{ b=t.getBBox(); }catch(e){ return; }
        if(!b.width) return;
        var over=Math.max(b.x+b.width-vb[2], b.y+b.height-vb[3], -b.x);
        if(over > 2) out.push({s:i+1,k:'svgtext',d:Math.round(over),t:t.textContent.trim().slice(0,40)});
      });
    });
    sl.classList.remove('active');
  });
  out.push({zooms: slides.map(function(sl){ return sl.getAttribute('data-fitted') || '-'; })});
  var d=document.createElement('div'); d.id='PROBE_RESULT';
  d.textContent=JSON.stringify(out); document.body.appendChild(d);
})();
"""


def check(path):
    path = os.path.abspath(path)
    probe_path = os.path.join(os.path.dirname(path), ".probe-" + os.path.basename(path))
    with open(path) as fh:
        page = fh.read()
    # the probe must run after the slide runner, and from the deck's own folder so ../assets resolves
    with open(probe_path, "w") as fh:
        fh.write(page.replace("</body>", "<script>" + PROBE + "</script></body>"))
    try:
        dom = subprocess.run(
            ["google-chrome", "--headless", "--disable-gpu", "--no-sandbox", "--window-size=1280,720",
             "--virtual-time-budget=4000", "--dump-dom", "file://" + probe_path],
            capture_output=True, text=True, timeout=90).stdout
    finally:
        os.remove(probe_path)
    m = re.search(r'id="PROBE_RESULT">(.*?)</div>', dom, re.S)
    if not m:
        print("PROBE FAILED  " + os.path.basename(path))
        return 1
    problems = json.loads(html.unescape(m.group(1)))
    zooms = [('%.2f' % float(z)) if z != '-' else '-' for z in problems.pop()['zooms']]
    slides = len(re.findall(r'<section class="slide', page))
    print("%-34s %2d slides  %d problem(s)" % (os.path.basename(path), slides, len(problems)))
    if zooms: print("    zoom per slide: " + " ".join(zooms))
    for p in problems:
        print("    slide %-3s %-8s +%-4spx %s" % (p["s"], p["k"], p["d"], p.get("t", "")))
    return len(problems)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    module = os.path.join(here, "..")      # the shared module sits beside this folder
    decks = sys.argv[1:] or sorted(glob.glob(os.path.join(module, "presentation", "t*.html")))
    sys.exit(min(sum(check(d) for d in decks), 255))
