### A

#### AMP
##### Contextual to [Exciter](#EXCITER_EXC) 
Amplificator. See [Shape](#SHAPE).

#### AMPLITUDE 
##### Contextual to [VCA](#VCA)
Base output gain. 

#### ARPEGGIATOR_ARP
##### Contextual to [Part Global](#PART_GLOBAL)
- This voice mode takes the notes of a held chord and automatically triggers the voice to play them one by one in a rhythmic sequence. 
    * *PATTERN* : Sequence direction : `UP / DOWN (DN) / UP+DOWN (U+D) / RANDOM (RND)`
    * *TEMPO / DIVISION (DIV)* : The tempo division control allows you to subdivide that master beat into precise mathematical fractions. A beat will be divided into 4, 8, or 16 parts. The triplets (denoted with a "T", e.g., 1/8T) fit three pulses into the exact space where two standard pulses would normally go. _Values:_ `1/4`, `1/8`, `1/8T`, `1/16`, `1/16T`, `1/32`.
    * *LENGTH (STEPS)* : truncate the pattern to a fixed number of steps. `Values: 1 to 64`. 
    * *VOICING* : Each step can be a single note or a voiced chord. `Values: MONO, MULTI, chord presets (MAJ, MIN, ...)`.
    * *LATCH* : Octave-span the pattern walks through. `Values: 1 to 8 octaves. HOLD` keeps the arpeggio going.  
    * *DYNAMICS (GATE)* : Fraction of each step the note sounds. `Values: 1 to 255. 128 = 50%`´ 

***Arpeggiator CV (CONTROL VOLTAGE)** and not MIDI. CV is an **analog**, physical standard. A CV arpeggiator generates raw, measurable electricity. To change the pitch of the arpeggio, it literally increases or decreases the voltage.*

#### AUDIO
##### Contextual to [Exciter](#EXCITER_EXC)
Continuous colored noise — beds, wind, breath, filter excitation. See [Shape](#SHAPE).

### B

#### BEHAVIOR
##### Contextual to [Panner](#PAN)
Select between two modes : linear (straight amplitude crossfade) or constant-power (a constante-power (-3 dB center) curve).
-  **NO PAN LAW** : Straight Amplitude Crossfade (Linear Panning)
- **How it Works:** The volume changes in a strict, straight mathematical line. If the panner is dead center, both the left and right speakers output exactly 50% of the signal's amplitude.
    
- **The Sonic Effect:** Because of how acoustic energy and human hearing work, two speakers playing at 50% amplitude do not sound as loud as one speaker playing at 100%. If you sweep a sound left and right using this setting, it will sound like the volume noticeably drops or loses energy every time it passes through the center.

-  **WITH PAN LAW** : Constant-Power (-3 dB Center) Curve
- **How it Works:** Instead of a straight line, the volume changes along a rounded, calculated curve (typically based on sine and cosine functions). When the panner is dead center, both speakers output at roughly 70.7% amplitude, which equals exactly a **-3 dB** reduction per channel.
    
- **The Sonic Effect:** When the acoustic power of two speakers playing at -3 dB is combined in a room (or in your headphones), they add up perfectly to 100% of the original perceived power. This eliminates the volume dip, ensuring the sound maintains a perfectly consistent, smooth loudness as it travels from hard-left to hard-right.

#### BIPOLR
##### Contextual to [Exciter](#EXCITER_EXC) 
See [Polarity_bipolr](#POLARITY_BIPOLR).

#### BP
##### Contextual to [Filter](#FILTER_FLT)
Band-pass. Allows only a specific "band" (or slice) of frequencies to pass through, simultaneously cutting both the extreme lows and the extreme highs outside of that slice.

### C

#### CHRD/CHORD
##### Contextual to [Part Global](#PART_GLOBAL)
Voice mode. Pressing a single key triggers an entire predefined chord rather than just a single note. The played note is the root; intervals add on top. Each chord tone consumes a [voice](#VOICE), so a MAJ7 chord uses four voices per key. 
    VOICING : Clickable text box (e.g., `MAJ ▼`) triggering a modal dropdown. Select the chord of your interest : `MAJ`, `MIN`, `MAJ7`, `MIN7`, `DOM7`, `DIM`, `AUG`, `SUS4`, `SUS2`, `PWR`, `OCT`, `5+OCT`.

#### CLICK :
See **[Toggle.](#TOGGLE)**

#### CLOCK 
##### Contextual to [Exciter](#EXCITER_EXC)
Toggle button (`SYNC`) enabling sample-accurate tempo latching.

#### COLOR/COL 
##### Contextual to [Exciter](#EXCITER_EXC) 
A mapped rotary knob selecting the spectral tilt.  _Values:_ `WHT`, `PNK`, `RED`, `BLU`, `VIO`. See https://en.wikipedia.org/wiki/Colors_of_noise for details.

### D

#### DAG
Direct Acyclic Graph. This is the graph in the middle of the main page, where nodes interact. 

#### DENSITY_DENS 
See [Rate](#RATE).

#### DETUNE
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
See [Pitch](#PITCH).

#### DLY_DELAY_STRUM
##### Contextual to [Part Global](#PART_GLOBAL)
DELAY mode generates multiple voices from a single note, with staggered onset times — a strum or echo-like effect created using actual voices rather than a delay line.
* TIME (Timing) : Stagger interval between successive voices.
* VOICES (Density) : The number of [voices](#VOICE) in the strum.
* DRIFT (Pitch) : Pitch drift added for each successive voice, to simulate human-style strumming detuning.

#### DRIFT
##### Contextual to [Exciter](#EXCITER_EXC)
Type of [Source](#SOURCE_SRC). This operates strictly in the sub-audio domain, providing slow, wandering modulation over seconds or minutes.

#### DRIVE
##### Contextual to [VCA](#VCA)
Not activated. 

#### DUO
##### Contextual to [Part Global](#PART_GLOBAL)
Duophonic mode. Two notes at a time. GLIDE (Portamento) doesn't affect the signal. 

#### DUST
##### Contextual to [Exciter](#EXCITER_EXC)
Sparse, randomly timed discrete impulses or clicks. Rather than a wash of noise, it sounds like a Geiger counter, static electricity, or the crackle of a worn vinyl record. See [Shape](#SHAPE_SHPE).

### E

#### ENGINE MODE
##### Contextual to [Part Global](#PART_GLOBAL)
Voice mode selection panel. 

#### ENVELOPE
A canvas-based interactive ADSR representation drawing mathematical curves.
To move the handles, click, hold down, and drag.

- **A (Attack) Handle**: tactile drag handle at the peak X/Y junction.
    
    - _Logic:_ Drags horizontally to adjust Attack time.
        
- **D (Decay) Handle**: tactile drag handle at the fall junction.
    
    - _Logic:_ Restricted to horizontal drag only.
        
- **S (Sustain) Handle**: tactile drag handle in the middle of the plateau.
    
    - _Logic:_ Restricted to vertical drag only (adjusts amplitude level).
        
- **R (Release) Handle**: tactile drag handle at the floor junction.
    
    - _Logic:_ Restricted to horizontal drag only.

**Curve Type Buttons `[C]`**: Three tiny click-cycle buttons stationed between the ADSR nodes enabling the selection of the curve shape. This lets you pair, say, a snappy exponential attack with a gentle logarithmic release.
    
- _Values:_ `-` (Linear), `L` (Logarithmic/concave), `E` (Exponential/convex), `S` (Sigmoid/S-curve).

#### EVOLUTION
Macro depth of the [LFO](#LFO). Depth of the drift layer (filtered chaos).

#### EXCITER_EXC
Node. The exciter taps a shared noise engine and shapes it.

### F

#### FILTER_FLT
The filter's user interface completely does away with traditional control buttons in favor of an interactive canvas that displays the amplitude response (an interactive filter curve visualizer) and plots a polyline in real time.
- **Character string** : A 4-way radio button strip across the top.
    - _Values:_ [`LP`](#LP) (Low-pass), [`BP`](#BP) (Band-pass), [`HP`](#HP) (High-pass), [`NCH`](#NCH) (Notch).
- **Cutoff / Resonance Handle**: **Drag and hold the little box on the line.** Dragging horizontally (X-axis) adjusts Cutoff. Dragging vertically (Y-axis, inverted) adjusts Resonance.
- [**Slope Badge**](#SLOPE): A click-cycle handle box in the top-right corner of the canvas to select the filter slope. 
    - _Logic:_ Clicking cycles through steepness cascades: **`6`, `12`, `18`, `24` dB/octave**
- **Bottom line** : A text row at the bottom displays integer-calculated estimates (e.g., "CUT 1.2kHz", "RES 45%", "24 dB/oct"). 
    - **"CUT 1.2kHz"** sets the specific frequency where the filter begins to do its job. 
    - **"RES 45%"** is the resonance value. 
    - **"24 dB/oct"** describes how aggressively the filter removes sound beyond the cutoff point. "24 dB/oct" means that for every octave you go above or under the 1.2 kHz cutoff, the volume of those higher or lower frequencies is reduced by **24 decibels**.

#### FM_DEPTH
##### Contextual to [Oscillator](#OSCILLATOR/OSC)

#### FREQUENCY
##### Contextual to [Filter](#FILTER/FLT)
Cutoff frequency. Logarithmic scale from `20Hz` to `20.0k`.
##### Contextual to [LFO](#LFO)
See [Rate](#RATE).


### G

#### GAIN_dB  
Spans from `-inf` to `-60.0dB` up to `+6.0dB`.

#### GLIDE
##### Contextual to [Part Global](#PART_GLOBAL)
Have no effect on the MONO, DUO and CHRD voices. Effective with LGT (Legato). 

### H

#### HP
##### Contextual to [Filter](#FILTER_FLT)
High-pass. Allows frequencies **above** the cutoff point to pass through, while aggressively cutting the frequencies **below** it.

#### HOVER HELP BAR 
The UI features a persistent one-line hint strip under the piano roll. Hovering over any control sets a contextual string (e.g., "Hover a control for help.").

### K

#### KNOBS 
Knobs are not standard rotary controls; they are rendered as 300-degree arcs (from 7 o'clock to 5 o'clock) with a 60-degree dead zone at the bottom. To use a knob, click, hold and drag up and and down. 

### L

#### LEVEL-LVL 
##### Contextual to [Exciter](#EXCITER_EXC) 
Continuous knob for output level (`LVL`).
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
See [Output](#OUTPUT).

#### LFO
**Graph node.** A multi-scale low-frequency oscillator—a “temporal synthesis engine” that generates three layers of modulation ([meso](#RYTHM), [micro](#TEXTURE), [macro](#EVOLUTION)) from a single shared phase, with organic chaotic drift and per-key synchronization. It shares the oscillator’s phase mechanism while adding an output with multiple levels of depth.

Because you cannot hear an LFO directly as audio, it is used exclusively as a **control signal**. Its purpose is to rhythmically modulate (automatically adjust) other parameters within a synthesizer over time. Think of an LFO as an "invisible hand" that continuously turns a specific knob back and forth for you at a steady, predictable pace.

#### LGT_LEGATO
##### Contextual to [Part Global](#PART_GLOBAL)
Monophonic voice mode. GLIDE TIME (Portamento) affects the legato between notes. 

#### LP
##### Contextual to [Filter](#FILTER_FLT)
Low-pass. Allows frequencies **below** the cutoff point to pass through untouched, while rolling off or cutting frequencies **above** that point.

### M

#### MAIN
##### Contextual to [Mixer](#MIXER_MIX)
Output gain. 
#### MAPPED ROTARIES 
Instead of dropdown menus, discrete enumerations (like noise color in **exciter** node) are selected via "mapped encoder knobs", where turning the knob snaps between string-labelled text values.

#### MIXER_MIX
Graph node. Usually auto-injected by the [DAG](#DAG) compiler when edges converge, rather than placed manually.
###### - OUTPUT / MAIN : Master gain
###### - MUTE / STATE : Silence the mix output
###### - [IN 1] : Input gain
###### - [CH 1] : Channel of the signal 

- **Auto-injection.** When you wire two oscillators into one filter input, the compiler places a mix er in front of the filter and routes the three sources through it. The patch's _post-compilation_ edge list (what the front panel draws) will show the injected mixer even though you didn't add it. You can add 6 inputs maximum. 

#### MODULATION 
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
Knob [FM DEPTH](#FM_DEPTH). **FM Depth** dictates the intensity of the frequency modulation being applied to an oscillator.

#### MONO
##### Contextual to [Part Global](#PART_GLOBAL)
Monophonic voice mode. GLIDE (Portamento) knob doesn't affect the signal.

#### MUTE
##### Contextual to [VCA](#VCA)
See [State](#STATE).
##### Contextual to [Mixer](#MIXER_MIX)
Silence the mix output. 

### N

#### NCH
##### Contextual to [Filter](#FILTER_FLT)
Notch. The exact opposite of a band pass filter. It drastically cuts a specific, narrow band of frequencies while allowing the lows and highs on either side to pass perfectly fine.

#### NOTE 
`C0` through `B`, where 1 internal step = 0.5 semitones.

### O

#### OSCILLATOR_OSC
Graph node. The primary tone generator with six [waveforms](#WAVEFORM), linear FM, pulse-width control, per-read detune, and intrinsic pitch glide.

#### OUTPUT
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
Output amplitude level spanning `-inf` to `+6.0dB`.

##### Contextual to [Mixer](#MIXER_MIX)
Output gain.

### P

#### PAN 
Graph node. Panner. Interpolates from `L100` to `C` (center deadzone) to `R100`. A panner (short for panoramic potentiometer) is a control that dictates the spatial positioning of a sound within the stereo field.

#### PART_GLOBAL 
Voice allocating engine. This panel manages how note data is distributed to voices.
- **How to access this panel ?**  Click on the "Voice P1" button at the top right corner of the graph panel or click anywhere on the dark background around the graph. 
- **Engine Modes :**
    - **MONO** : Monophonic mode. GLIDE (Portamento) knob doesn't affect the signal.
    - **LGT (Legato)** : Monophonic mode. GLIDE TIME (Portamento) affects the legato between notes. 
    - **POLY** : Polyphonic mode. Play up to 128 notes simultaneously. The default for most patches. 
    - **UNI (Unison)** : Takes some or all available voices and stacks them onto a single keypress. The voices are often slightly detuned from one another to create a massive, thick, and wide sound. 
        *VOICES (DENSITY)* : increases the number of [voices](#VOICE) per key. 
        *SPREAD (DETUNE)* : increases the pitch difference between each voice.
    - **DUO** : Polyphonic mode. Two notes at a time. GLIDE (Portamento) doesn't affect the signal. 
    - **CHRD (Chord)** :  Pressing a single key triggers an entire predefined chord rather than just a single note. The played note is the root; intervals add on top. Each chord tone consumes a [voice](#VOICE), so a MAJ7 chord uses four voices per key. 
        *VOICING* : Clickable text box (e.g., `MAJ ▼`) triggering a modal dropdown. Select the chord of your interest : `MAJ`, `MIN`, `MAJ7`, `MIN7`, `DOM7`, `DIM`, `AUG`, `SUS4`, `SUS2`, `PWR`, `OCT`, `5+OCT`.
    - **DLY (Delay Strum)** : DELAY mode generates multiple voices from a single note, with staggered onset times — a strum or echo-like effect created using actual voices rather than a delay line.
        *TIME (Timing)* : Stagger interval between successive voices.
        *VOICES (Density)* : The number of [voices](#VOICE) in the strum.
        *DRIFT (Pitch)* : Pitch drift added for each successive voice, to simulate human-style strumming detuning.
    - **ARP (Arpeggiator)** : Arpeggiator CV (CONTROL VOLTAGE) and not MIDI.
     This voice mode takes the notes of a held chord and automatically triggers the voice to play them one by one in a rhythmic sequence. 
        * *PATTERN* : Sequence direction : `UP / DOWN (DN) / UP+DOWN (U+D) / RANDOM (RND)`
        * *TEMPO / DIVISION (DIV)* : The tempo division control allows you to subdivide that master beat into precise mathematical fractions. A beat will be divided into 4, 8, or 16 parts. The triplets (denoted with a "T", e.g., 1/8T) fit three pulses into the exact space where two standard pulses would normally go. _Values:_ `1/4`, `1/8`, `1/8T`, `1/16`, `1/16T`, `1/32`.
        * *LENGTH (STEPS)* : truncate the pattern to a fixed number of steps. `Values: 1 to 64`. 
        * *VOICING* : Each step can be a single note or a voiced chord. `Values: MONO, MULTI, chord presets (MAJ, MIN, ...)`.
        * *LATCH* : Octave-span the pattern walks through. `Values: 1 to 8 octaves. HOLD` keeps the arpeggio going.  
        * *DYNAMICS (GATE)* : Fraction of each step the note sounds. `Values: 1 to 255. 128 = 50%`´ 

#### PITCH
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
Spans ±1 semitone (~1 cent per step) for analog fan-out without disturbing glide targets.

#### POLARITY_BIPOLR
##### Contextual to [Exciter](#EXCITER_EXC)
Bipolar swings the output around zero rather than unipolar.
Toggle button (`BIPOLR`) switching between unipolar and bipolar output.

#### POLY
##### Contextual to [Part Global](#PART_GLOBAL)
Polyphonic voice mode. Play up to 128 notes simultaneously. The default for most patches. 

#### POSITION
##### Contextual to [Panner](#PAN)
Define stereo placement from L (left) to R (right) with a center (c).

### Q

#### QUANT
Sample & hold quantized, random wevaform. A noise quantized following some musical grid. See [Shape](#SHAPE-SHPE).

### R

#### RATE
##### Contextual to [Exciter](#EXCITER_EXC)
A continuous knob setting the speed/density. _Logic:_ Relabels to `[ DENSITY ]` (`DENS`) automatically if _Source_ is set to `DUST`; otherwise displays `[ RATE ]`.
In the sub-audio range : approx. 0.05Hz to 40Hz.
##### Contextual to [LFO](#LFO)
A continuous knob setting the speed/density.
Renders in centi-Hz, spanning `0.05Hz` to `40.00Hz`.

#### RYTHM
Meso depth of the [LFO](#LFO). 

### S

#### SATURATE
##### Contextual to [VCA](#VCA)
Not activated.

#### S&H
Sample and hold

#### SHAPE_SHPE 
##### Contextual to [Exciter](#EXCITER_EXC)
A continuous knob modifying the source. _Logic:_ Relabels to `[ AMP ]` (for DUST), `[ STEPS ]` (for QUANT), `[ SLEW ]` (for DRIFT), or `[ SHAPE ]` (default).

#### SLEW
##### Contextual to [Exciter](#EXCITER_EXC)
See [Shape](#SHAPE_SHPE).
##### Contextual to [LFO](#LFO)
Rate inertia. Higher values cause the velocity itself to change gradually rather than in jerks.

#### SLOPE
##### Contextual to Filter
A **cascade slope engine** is a flexible filter architecture that routes an audio signal through multiple consecutive filtering stages (referred to as "poles") in series.

-  Principle of Operation

Every individual pole within the cascade attenuates the frequency spectrum by a fixed rate of **6 dB per octave**. By stacking these stages, the engine increases the steepness of the filter's roll-off curve.

- **1-Pole (6 dB/oct):** Provides a gentle, gradual attenuation.
    
- **2-Pole (12 dB/oct):** Provides a moderate slope, commonly used for bright, natural-sounding patches.
    
- **3-Pole (18 dB/oct):** Provides a pronounced, steep slope.
    
- **4-Pole (24 dB/oct):** Provides a highly aggressive slope, standard for deep bass and focused lead synthesis.

#### SOURCE_SRC 
##### Contextual to [Exciter](#EXCITER_EXC)
A mapped rotary knob selecting the randomness family. _Values:_ `AUDIO`, `DUST`, `S&H`, `QUANT`, `DRIFT`.

#### SPREAD - SPRD
##### Contextual to [Exciter](#EXCITER_EXC)
At zero spread, identical noise is sent to both speakers (pure mono). As Spread increases, the left and right channels generate mathematically independent noise streams.
- **Sonic Effect:** Creates a massive, enveloping "wash" of sound. It is ideal for widening cymbal and hi-hat synthesis or generating immersive, airy wind textures.

#### STATE
##### Contextual to [VCA](#VCA)
Forces audible silence (executes but emits zero).
##### Contextual to [Mixer](#MIXER_MIX)
Silence the mix output. 

#### STEPS 
##### Contextual to [Exciter](#EXCITER_EXC)
See [Shape](#SHAPE/SHPE).

#### SYNC
##### Contextual to [Exciter](#EXCITER_EXC)
See [Clock](#CLOCK).

### T

#### TACTILE DRAG 
See [**Knobs**](#KNOBS).

#### TEXT ENTRY 
Uses a modal input capturing text input, featuring a blinking cursor. It strictly filters out non-filesystem-safe characters (e.g., `/`, `\`, `:`, `*`, `?`, `<`, `>`, `|`).

#### TEXTURE
Micro depth of the [LFO](#LFO). 

#### TIMBRE
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
Width knob. Adjusts the pulse width of the Pulse shapes.

#### TIME
In ms/s. Logarithmic scale from `1ms` to `10.0s`.

#### TOGGLE
Toggles execute exactly on the click edge frame within an evaluated hitbox. Exemple of toggle : BIPOLR (Exciter) or SYNC (Exciter)

### U

#### UNI_UNISON
##### Contextual to [Part Global](#PART_GLOBAL)
Voice mode. Takes some or all available [voices](#VOICE) and stacks them onto a single keypress. The voices are often slightly detuned from one another to create a massive, thick, and wide sound. 
* VOICES (DENSITY) : increases the number of [voices](#VOICE) per key. 
* SPREAD (DETUNE) : increases the pitch difference between each [voices](#VOICE).


### V

##### VCA
Graph node. The voltage-controlled amplifier: the level/gate stage of a voice.

#### VOICE
In synthesizer terminology, a **voice** is the complete, independent hardware or software signal path required to generate and shape a single musical note at a given time. The GDVP is set at 128 voices during compilation (which means that the user cannot set the maximum number of voices themselves).

### W

#### WAVEFORM
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
Six waveforms : sine (SIN), square (SQR), triangle (TRI), sawtooth (SAW), pulse (PLS) and noise (NOS). 
- **Pulse** needs the timbre value to be above 0 to work. A pulse wave is essentially a square wave where the symetrical shape has been pushed off-center (the "on" and "off" times are unequal). As the pulse becomes narrower, the sound shifts from a hollow tone to a very thin, nasal, and pinched character.
- A **noise** waveform is a completely aperiodic, chaotic signal. Instead of generating a single pitched musical note, noise simultaneously blasts thousands of random frequencies. It sounds like a rushing waterfall, analog television static, or hissing wind. 
     - **This particular noise waveform is chromatic. This means that sound is not just random noise. It is random noise generated around a pitch.** 
##### Contextual to [LFO](#LFO)
Six waveforms : sine (SIN), square (SQR), triangle (TRI), sawtooth (SAW), sample & hold (S&H) and noise (NOS). 

#### WIDTH
##### Contextual to [Oscillator](#OSCILLATOR_OSC)
See [Timbre](#TIMBRE).