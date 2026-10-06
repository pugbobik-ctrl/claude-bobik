# Review of the three place-card dielines (D1 cross-slot, D2 form-and-void, D3 one-sheet tents)

Method: I re-derived the numbers from src/d1.py, d2.py, d3.py and the verify.txt files (formulas re-computed by hand, not trusting the notes) and looked at all PNGs. Nothing in dielines/ was modified.

Common assumptions I checked: board 400 g/m2, caliper 0.50 mm; all pieces weigh only 3-6 g (area x 0.4 mg/mm2): D1 about 2.7 g, D3 tent about 4.5 g, D2 whole card about 6 g. Sliding friction on linen (mu about 0.3-0.5) therefore starts at roughly 1-2 gf for all three; tip-over angles in the notes (61 deg, 42 deg) are real but irrelevant, because every card slides or is carried away long before it tips. What matters is the failure MODE after a nudge or a grab (separates / collapses / stays one body).

Legibility (eye 40 cm away, line of sight 30 deg down; apparent cap height = cap x cos(angle between sightline and face normal)):
- D1 A: vertical plate, angle 30 deg, cos 0.87; cap 5.1 mm -> 4.4 mm -> 0.63 deg = 38 arcmin. Best of the three.
- D3 F leaf: leaf at 72 deg, i.e. leans back 18 deg, so normal points 18 deg up, angle 48 deg, cos 0.67; 5.1 -> 3.4 mm -> 29 arcmin. OK.
- D2 S: 75 deg, angle 45 deg, cos 0.71; cap 4.9 -> 3.4 mm -> 30 arcmin. OK.
- All names pass (>= 25-30 arcmin). All SECONDARY lines fail: D3 "TABLE 4 . SEAT nn" is 2.5 mm type (cap 1.8 mm -> 1.2 mm apparent = 10 arcmin), "DINNER . date" 2.3 mm (D2 and D3), D2 event line 2.2 mm. The seat number is the one thing a guest does need, and it is set below comfortable reading size in D2 and D3. Minimum 3.5 mm type (cap 2.5) for seat/table.

---------------------------------------------------------------------
## D1 - two plates on slots

Verdict: sound, easiest to make well, best name legibility, but the weakest as a "form". Fix the centre-line and the footprint and it is a good, quiet object.

Top problems (ranked)
1. The seat plate B cuts the name in half. B stands at x = 0 and its top at the centre is z = 26; the name is centred on x = 0 with cap top z = 26.1 and baseline 21. In the assembled render the hairline of B runs through "Zh". From any lateral offset B's face also hides a sliver of the name (sight line grazes B's top at 26-34 mm). Fix: raise the name so it sits fully above B: baseline z = 27, cap top 32.1 (dome at x = 38 is 38.8, so margin 6.7; check at 20 chars x = 37.8). Move the small "DINNER . date" line below the name (z about 20) or onto B. Or drop B's centre height to 22 and slot depth to 7.2 (play angle then 1.6 deg, worse) - raising the name is better.
2. Slot width under steel rule. 0.70 "slot" = 2 pt rule (0.71) assumes the rule removes a 0.7 gap. A single rule does not remove material; it displaces fibre and uncoated 400 g board springs back, so a real single-rule slit ends up about 0.35-0.55 wide - narrower than the 0.50 board + friction = binding or no assembly. A 0.7 mm waste strip cannot be stripped. Practice: (a) die-maker supplies a 1.0-1.07 mm (3 pt) rule or two rules 0.7 apart with a stripping pin, or (b) laser, drawing 0.50-0.55 + kerf (0.2) = 0.7-0.75 net, accepting brown scorch on the lemon edge (visible next to a yellow face, much less on black), or (c) CNC knife: a 0.7 sliver stays in; two passes plus a pick. Plan: first sheet carries slots at 0.60 / 0.70 / 0.80 / 0.90 on the 15 sets; choose by fit. Also add a 1.2-1.5 mm radius or small relief at the slot end (right now square end; board 0.5 mm wedged in a 15 mm slot tears from the slot end).
3. Footprint 100 x 88 mm is large for a card that carries 6 characters of information; B's two 44 mm arms reach into the plate and toward the guest. Fix: shorten B to 64 wide (arms 32) and keep tip-over >= 55 deg (rhombus inradius 50x32/sqrt(50^2+32^2) = 27 mm; atan(27/18.4) = 55.7 deg). Or make B asymmetric (front arm 18, rear arm 38) so the cross sits right above a plate rim.
4. B's print is edge-on to the guest. B's faces face left/right, so the guest cannot read her own TABLE/SEAT (0 deg); only neighbours and servers can. Either accept (it is for the waiter) or print the table number on A's lower margin.
5. Lead-in 2.3 wide x 1.5 long square-ended is a delicate little rule bend (rule radius minimum about 1.5-2 mm on a 2 pt rule); also the 0.2 mm bottoming gap between the plates is below the die/laser tolerance of about 0.1-0.2 mm -> specify 0.6 mm (A slot 15.0, B floor 14.4; the play angle becomes 1.0 deg, still fine).
6. Two loose parts per guest (notes already admit). With duplex digital print of 400 g (0.5 mm) most SRA3 digital presses top out at 300-350 gsm / 0.40-0.45 mm; check the press or print litho / use 350 g and re-cut the slot to 0.6 caliper.

Checks that hold: dome R119.1 sagitta 11 on 100 mm, dip same radius (nests: verified); slot-to-slot play 0.76 / 1.02 deg re-derived (atan(0.2/15), atan(0.2/11.2)); rhombus inradius 33.0 mm, tilt 60.9 deg; grain parallel to the 450 side = standard long-grain SRA3, vertical on both plates (stiff against being pushed over); sheet utilisation 69.5 %.

Fixes in numbers: name baseline z 27; B 64 wide (or 20/44 asymmetric); slot test series 0.60-0.90; slot-end relief; bottom gap 0.6.

Concept: Reads as arch-topped plaque + hairline fin. The dome/dip echo is hidden (it exists only in the imposition nesting). Not blobby, not receipt-like - except that B's "TABLE | SEAT" in two boxes looks like a ticket stub (split label); keep it as one line. Visually the weakest silhouette of the three.

Bold improvement: make B a tall "sail" and give the pair a role split: B stands 70 mm tall behind the name (T-joint at the rear edge of A, A 100 x 34 low), carries a 55-60 mm table numeral readable across the room, and its top edge keeps the dip arc; the name sits low on the plate - a ship's nameplate under a sail. Rows of sails down the table make the table readable from the door. Rear arm 55 mm so the T stays stable (check COM against a 100 x 55 base).

---------------------------------------------------------------------
## D2 - form and its void

Verdict: the strongest idea and the most photogenic (the segment rising out of its own hole), but it is the largest, most breakable, and the flat state looks like a ticket. Worth taking forward as a compact variant.

Top problems (ranked)
1. Footprint 105 x 148 mm A6 on the table per guest. A dinner place has maybe 150-200 mm free in depth above the plate; a 148 mm-deep rounded card with two holes eats the cutlery/glass zone and sits on top of nothing. The lifted part has only a 90 x 24 mm base. Fix: compact variant (not drawn by the author, I computed it): S chord 80, height 32; b = 40 (c1 to c2); crown at (32 cos75, 32 sin75) = (8.28, 30.91) from c1; P = hypot(40-8.28, 30.91) = 44.3 mm at 44.3 deg (same angle as now); depth = front strip 20 + S 32 + web 8 + P 44.3 + lip 6 + rear margin 7 = 117 -> card 105 x 117 (21 % smaller). Keep S 90 wide if the name needs it (chord 90, height 32 gives R 33.7: check cap-top clearance).
2. The strut is a flat 40 x 55 x 0.5 mm strip in compression. Euler load 2.3-4.6 N (re-derived: pi^2 E I / L^2 with I = 40 x 0.5^3 / 12 = 0.42 mm4, E 2000, L 55.4 = 2.7 N); a push H at the crown loads P with 1.11 H (re-derived statics), so buckling at about 2 N horizontal; real boards with creased ends are weaker. That is 200 gf = a finger pressing the S plate, very easy. (It will not happen on a bump because the card slides at about 2.5 gf first, but a guest pressing the crown while pulling the card, or a waiter's tray, will.) Failure mode is benign (flops flat, can be re-lifted), but it will be fiddled with. Fix: add 5 mm side flanges to P (two extra creases at 5 mm from each edge; I about 10.8 mm4 = 25x) - or two 15 mm wide struts at x = +/-10 that make a ladder; or shorten L (buckling ~ 1/L^2).
3. Fold angles: c2 is 135.7 deg and c3 119 deg from flat on a 0.5 mm board - sharp folds, c2 only 40 mm long. Crease cracking on uncoated black-on-yellow is minor, but the P's effective length changes with the number of 135 deg folds (take-up about 0.3-0.4 mm per fold) - +/-0.5 mm on P = +/-0.8-1.5 deg lean, as stated, and fold take-up alone can exceed that. Specify a lead-in tolerance on P length and test; consider making the strut longer by 0.5 and letting S lean 73-75 deg.
4. Printing collisions and sizes: the "DINNER . 10.10.2026" line sits at v = 33 (cap 1.6) while the lip covers v = 34-40 over 24 mm centered - 0.7 mm overlap, and the guest sees the lip on top of the line (the render shows it). Move the line to v = 30 or drop it. Event line on the flat card 2.2 mm = invisible. The back of S (visible to the opposite guest) is blank unless printed duplex; and the hole exposes the table linen: plan it.
5. Hinge corner tear risk: at the c1 ends the arc meets the chord at about 83 deg; the crease extends 0.5 mm past as "tear stop" - OK for a die, but add a 1 mm radius/small notch at the cut/crease junction, otherwise the card tears there on the first lift (stress concentration).
6. Ticket/receipt: a rounded-corner (R3) A6 rectangle with a banner line, a "TABLE 4 . SEAT 07" strip along the edge and two punched-out windows reads as a ticket/boarding card in its flat state. The folded form is not, but staff will hand out the flat state. Fix: drop the R3 corners (use a die-cut outer trim that is the S/P-driven shape, or a straight trim), delete the "TABLE . SEAT" strip and put table/seat on S.
7. Print bleed: "holes need none" is right if yellow is flooded across both sides of the cut; on pre-coloured board no bleed anywhere. Fine.

Checks that hold: triangle closes (re-derived: S crown at (40 cos75, 40 sin75) = (10.35, 38.64) from c1; P tip at 50 - 55.36 cos44.3 = 10.35); voids to edge 7.5 mm, web 10 mm (above the 3 mm die minimum); grain parallel to the 105 side = creases parallel to grain and 450 mm side on the SRA3 8-up (standard long grain); fits C6.

Concept: genuinely its own idea; void is legible; not blobby (circle segment + trapezoid); good. Risk: reads like a "pop-up greeting card" - the half-moon also resembles a standard arched card; the flat state resembles a ticket.

Bold improvement: make the void do the printing work: print the reverse of the card black, set the card on a black table runner (or give a black underlay square), so the two voids read as black shapes beside their lemon twins. Then S is lemon-on-black from behind. With black linen the concept becomes a graphic (positive / negative), not only a mechanism. Also use the reverse of S for the opposite guest.

---------------------------------------------------------------------
## D3 - one sheet for the whole table

Verdict: the best-engineered and most robust (closed triangle, self-correcting tab, 12/sheet, 88 % use), but the concept is invisible once the cards are on the table, and the form is the stock tent card. It is the safest event solution and the weakest idea. Two production claims are wrong.

Top problems (ranked)
1. The whole-table principle does not survive. 12 pieces: widths 94-106 mm, sagitta 3-6 mm on R235-470 arcs; the four tents in d3_assembled are rectangles of near-identical outline, and the differences exist only on the two side edges (about 2-3 mm of bow, 12 mm of width variation over 100). Seats are 600+ mm apart so no one sees the pieces "fit". The flat sheet that works as a table plan exists only before the dinner and after - and nobody puts 12 folded tents back in their holes. What a viewer sees: a standard hotel tent card with a 2.4 mm TABLE/SEAT caption. Fix: make the difference large and straight (Mari-like polygons): cut lines with real skew: leaf outlines as trapezoids/parallelograms (side edges inclined +/-6-12 deg, i.e. 10-20 mm offset between top and bottom of a 36 mm leaf) - tessellation stays zero-waste (all cut lines straight, each shared). Then the 12 tents have 12 clearly different gables.
2. Grain. Creases run along the 320 mm side; grain parallel to creases is correct for folding but means short-grain SRA3 (grain along 320), which is a special order for 400 g; standard SRA3 is grain-long (450). Folding across the grain on 0.5 board cracks. Fix: either order SRA3 short-grain, or rotate the mosaic: 4 pieces along the 450 side x 3 rows along 320: width 100-106 fits 4 x 106 = 424 along 450, and 3 strips x <= 102 along 320 = 306 <= 308 usable - which needs strip length 106 -> 102: leaf 34.5, flap 12, B 21 (depth 21.3, height 32.8). Tight but feasible and it keeps grain parallel to creases on a standard sheet.
3. "One pass with a combined cutting + creasing die" is not true as specified: creases 1-4 are scored from the back (mountain), crease 5 from the printed face (valley). A flatbed die creases from one side only. Fix: score all five from the back and fold the fold-over (crease 5, hidden under the roof) against its score - it is invisible; or drop the fold-over altogether (see 5).
4. Crease 4 and crease 5 are 2.0 mm apart. With a 0.71 rule and counter channel (2 x 0.5 + 0.71 = 1.7 mm channel) there is 0.3 mm wall: impossible; minimum crease pitch about 3 mm. Fix: riser 3.0, tab 6.5 (tab fold-over 3.5 stays), or remove crease 5 and use a plain 2-4 mm riser tab.
5. Zero-gap mosaic die-cutting. It is real, but: (a) every rule is a zero-kerf kiss - fine; (b) nothing holds the 12 pieces in the sheet after a through-cut - without nicks they are loose, with nicks you need 4 nicks x 15 lines = 60 breaks and each break leaves a white fibre burr on a yellow edge; choose through-cut and deliver in a tray. (c) The "pieces go back in their holes" claim relies on this; it is not robust. (d) Plotter: a 5-pass minimum (10 odd nodes) is right; with drag knife radius compensation the tab/notch inner corners need an overcut 1-1.5 mm that notches the neighbour: use a tangential oscillating knife or laser. (e) Laser: kerf 0.2 per cut, shared lines become gaps of 0.2 (acceptable) but the scorch darkens the shared edge of both pieces.
6. Assembly is the fiddliest of the three: flap must be slid UNDER an already folded B, tab (18 x 0.5, 2 mm riser) threaded up a 0.7 slit, and folded 3.5 mm back - in a 22 mm deep cavity. Real time 40-60 s per card for the first dozen (notes: 20-30 s); staff pre-assemble, but cards then no longer stack flat (34 mm high). Order/test 12 pieces first (the notes say this).
7. Print: seat caption 2.5 mm; DINNER 2.3 mm: too small (above). The cavity behind F means the text at 7 mm above the foot is at 6.7 mm table height, hidden by cutlery.

Checks that hold: tent 36 mm at 72 deg: height 34.24, depth 22.25 (re-derived 2 x 36 x cos72); closure 13.0 + 9.25 (depth is set by the tab, tolerance self-corrects: 0.5 mm depth error = 0.4 deg); feet +/-11.1, COM 11.8 -> 42 deg; slit 19.5 x 0.7 vs tab 18 x 0.5, slit ends >= 20 mm from edges; 0.2 clearance for ONE layer is right; 5.9 mm slit-to-notch web OK; B 21 ends 1.25 mm short of the foot.

Concept: honest rating: weak as a visible idea; the logistics idea (one sheet = one table, seat numbers in reading order = the plan) is good and could be sold as such. Gentle S-curves across the sheet drift toward the "soft wavy" of the poster lettering; the micro-captions DINNER . date / TABLE . SEAT nn drift toward ticket text, as in D2.

Bold improvement: make the difference big and printable: straight-cut skewed polygons (Mari), AND print one continuous heavy black line (a single 2 mm stroke) across the whole sheet that runs over the K (rear) leaves, so each tent shows a fragment of a larger drawing; at the table the neighbours' fragments never meet, but when the pieces are collected they complete it - give the staff a reason to return all 12. Put the table plan (seat 01-12 as outlines) on the backs of the flap/B (hidden) only.

---------------------------------------------------------------------
## Recommendation

Take forward D2 (compact variant, stiffened strut, ticket-free flat state, black-reverse/black-runner idea) as the hero direction: it is the only one that is plainly its own idea and looks like nothing on the poster or the table runners.

Take forward D1 as the robust second (fix the name/B collision, shorten B, test slot widths); it can nest on the same sheet and is the cheapest to make well.

Shelve D3 unless the client weighs logistics (one sheet per table) above form; if kept, the skewed-polygon + grain + crease fixes above are mandatory. If one direction must be the "will not fail on the night", it is D3 - but then call it what it is: a tent card with a clever sheet.

## Production checklist for any of them
- Digital print weight: check press max weight (many top out at 300-350 g / 0.45 mm); 400 g (0.50 mm) usually means litho/screen/flat-bed digital.
- Pre-coloured lemon board is better than flood-printed yellow (no bleed, no scuff on folds, cracks invisible). If flooded, 3 mm bleed on outer trim only (agree with D2/D3 notes).
- Always run a first-article test of 12 sets before the run; test slot widths 0.6-0.9 (D1), P-length +/-0.5 (D2), tab fit (D3).
