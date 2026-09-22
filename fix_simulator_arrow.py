import re

with open("simulator.html", "r") as f:
    html = f.read()

# Replace the single arrow with two arrows in the SVG
arrow_svg = '<line id="transitionArrowTop" marker-end="url(#arrow)" stroke="#8ed5ff" stroke-width="2" x1="280" x2="280" y1="120" y2="87"></line>\n              <line id="transitionArrowBottom" marker-end="url(#arrow)" stroke="#8ed5ff" stroke-width="2" x1="280" x2="280" y1="130" y2="163"></line>'
html = re.sub(r'<line id="transitionArrow".*?></line>', arrow_svg, html)

# Replace the JS that updates the arrow
old_js = """      const arrow = document.getElementById('transitionArrow');
      arrow.setAttribute('y1', homoY);
      arrow.setAttribute('y2', lumoY + 10);"""

new_js = """      const midY = (homoY + lumoY) / 2;
      const arrowTop = document.getElementById('transitionArrowTop');
      if (arrowTop) {
        arrowTop.setAttribute('y1', midY - 16);
        arrowTop.setAttribute('y2', lumoY + 10);
      }
      const arrowBot = document.getElementById('transitionArrowBottom');
      if (arrowBot) {
        arrowBot.setAttribute('y1', midY + 16);
        arrowBot.setAttribute('y2', homoY);
      }"""
html = html.replace(old_js, new_js)

# Remove the 'const midY = (homoY + lumoY) / 2;' that was originally AFTER the arrow update, 
# since we just moved it BEFORE the arrow updates.
# Wait, let's just replace the exact block.
old_midy_js = """
      const midY = (homoY + lumoY) / 2;
      document.getElementById('egBadgeBg').setAttribute('y', midY - 12);
"""
new_midy_js = """
      document.getElementById('egBadgeBg').setAttribute('y', midY - 14); // slightly bigger badge
"""
html = html.replace(old_midy_js, new_midy_js)

# Also update the badge height from 28 to 28 (it was 28). wait, if y is midY-14, height should be 28 to be centered.

# Shift photon wave JS
old_wave_js = """      const wavePath = document.getElementById('photonWave');
      wavePath.setAttribute('d', `M 285,${midY} Q 295,${midY-10} 305,${midY} T 325,${midY} T 345,${midY}`);
      const poly = document.querySelector('#photonParticle polygon');
      if (poly) poly.setAttribute('points', `348,${midY} 340,${midY-5} 340,${midY+5}`);
      const photonLabel = document.getElementById('photonLabelText');
      if (photonLabel) {
        photonLabel.setAttribute('y', midY + 3);
        photonLabel.textContent = `hν (${wavelength} nm)`;
      }"""

new_wave_js = """      const wavePath = document.getElementById('photonWave');
      wavePath.setAttribute('d', `M 350,${midY} Q 360,${midY-10} 370,${midY} T 390,${midY} T 410,${midY}`);
      const poly = document.querySelector('#photonParticle polygon');
      if (poly) poly.setAttribute('points', `413,${midY} 405,${midY-5} 405,${midY+5}`);
      const photonLabel = document.getElementById('photonLabelText');
      if (photonLabel) {
        photonLabel.setAttribute('x', '420');
        photonLabel.setAttribute('y', midY + 3);
        photonLabel.textContent = `hν (${wavelength} nm)`;
      }"""
html = html.replace(old_wave_js, new_wave_js)

# Also update the initial SVG photon wave coords
old_svg_photon = """<path d="M 285,119 Q 295,109 305,119 T 325,119 T 345,119" fill="none" id="photonWave" stroke="#ffc640" stroke-linecap="round" stroke-width="3"></path>
                <polygon fill="#ffc640" points="348,119 340,114 340,124"></polygon>
                <text class="font-label-sm text-[12px]" fill="#ffc640" id="photonLabelText" x="355" y="123">hν (590 nm)</text>"""

new_svg_photon = """<path d="M 350,119 Q 360,109 370,119 T 390,119 T 410,119" fill="none" id="photonWave" stroke="#ffc640" stroke-linecap="round" stroke-width="3"></path>
                <polygon fill="#ffc640" points="413,119 405,114 405,124"></polygon>
                <text class="font-label-sm text-[12px]" fill="#ffc640" id="photonLabelText" x="420" y="123">hν (590 nm)</text>"""
html = html.replace(old_svg_photon, new_svg_photon)

with open("simulator.html", "w") as f:
    f.write(html)
