data = {
    'topic': 'How India Reached 3rd Stage Fast Breader Reactor',
    'information': 'India’s Fast Breeder Reactor (FBR) program is a cornerstone of its three-stage nuclear energy strategy, initiated by Dr. Homi Jehangir Bhabha in the 1950s. The program aims to transition from uranium dependence to thorium utilization, leveraging India’s limited uranium reserves and vast thorium deposits. The first stage involves Pressurized Heavy Water Reactors (PHWRs) using natural uranium, producing plutonium as a byproduct. The second stage, represented by the Prototype Fast Breeder Reactor (PFBR) at Kalpakkam, uses plutonium and uranium to breed more fissile material, including uranium-233 for the third stage. The third stage envisions thorium-based reactors, enabling India to harness its abundant thorium reserves (25% of global reserves) for long-term energy independence and reduced reliance on uranium imports. The PFBR, designed by the Indira Gandhi Centre for Atomic Research (IGCAR) and constructed by Bharatiya Nabhikiya Vidyut Nigam Ltd (BHAVINI), achieved first criticality on April 6, 2026, after a 20-year delay and significant cost overruns. Construction began in 2004, but technical challenges such as sodium leaks, fuel handling issues, and material failures caused repeated delays and escalated costs from ₹3,492 crore to over ₹8,181 crore. The PFBR uses uranium-plutonium mixed oxide (MOX) fuel and a uranium-238 blanket to breed plutonium-239, producing uranium-233 for thorium-based reactors in the third stage. This aligns with India’s goal of achieving a closed fuel cycle, significantly enhancing energy security. The program’s success reflects India’s advancements in indigenous nuclear technology and adherence to its self-reliance policy, *Atmanirbhar Bharat*. Despite international restrictions due to its exclusion from the Nuclear Non-Proliferation Treaty (NPT), India developed its own materials and safety protocols, positioning itself as a leader in advanced nuclear technology. The PFBR’s success contributes to India’s goal of reaching 100 GW of nuclear power by 2047, reducing uranium imports, and paving the way for thorium-based reactors. The program’s long-term vision includes achieving a closed fuel cycle, ensuring sustainable energy production for centuries using thorium reserves, and aligning with India’s broader energy security and net-zero emissions goals by 2070.',
    'script': [
        {'id': 1, 'script': 'On April sixth, twenty twenty-six, India’s Prototype Fast Breeder Reactor at Kalpakkam achieved first criticality after two decades of delays.'},
        {'id': 2, 'script': 'The reactor, designed by the Indira Gandhi Centre for Atomic Research and built by BHAVINI, faced sodium leaks, fuel handling issues, and material failures.'},
        {'id': 3, 'script': 'Costs soared from three thousand four hundred ninety-two crore rupees to over eight thousand one hundred eighty-one crore rupees during its construction, which began in two thousand four.'},
        {'id': 4, 'script': 'It uses uranium-plutonium mixed oxide fuel and a uranium-238 blanket to breed plutonium-239 and uranium-233 for thorium reactors.'},
        {'id': 5, 'script': 'This marks India’s transition to the second stage of its three-stage nuclear program, initiated by Doctor Homi Bhabha in the nineteen fifties.'},
        {'id': 6, 'script': 'The goal is to leverage India’s vast thorium reserves—twenty-five percent of the world’s supply—for long-term energy independence.'},
        {'id': 7, 'script': 'Despite exclusion from the Nuclear Non-Proliferation Treaty, India developed its own materials and safety protocols.'},
        {'id': 8, 'script': 'The PFBR’s success brings India closer to one hundred gigawatts of nuclear power by twenty forty-seven and a closed fuel cycle for centuries.'}
    ]
}


for script in data["script"]:
    id = script["id"]
    script = script["script"]

    print(f"ID: {id}")
    print()
    print(f"SCRIPT: {script}")
    print()
    print("*"*50)
