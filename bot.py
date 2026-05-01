def compose(category, merchant, trigger, customer=None):

    # -------------------------------
    # STEP 1: Customer message case
    # -------------------------------
    if customer is not None:
        cust_name = customer.get("identity", {}).get("name", "Customer")
        merchant_name = merchant.get("identity", {}).get("name", "your clinic")

        body = (
            f"Hi {cust_name}, {merchant_name} here 🦷 "
            f"Aapka checkup due hai. Want to book a slot this week?"
        )

        return {
            "body": body,
            "cta": "open_ended",
            "send_as": "merchant_on_behalf",
            "suppression_key": trigger.get("id", "no_id"),
            "rationale": "Customer reminder"
        }

    # -------------------------------
    # STEP 2: Merchant data (SAFE)
    # -------------------------------
    identity = merchant.get("identity", {})
    performance = merchant.get("performance", {})
    peer_stats = category.get("peer_stats", {})

    name = identity.get("name", "Merchant")
    locality = identity.get("locality", "")
    city = identity.get("city", "")

    ctr = performance.get("ctr", 0)
    peer_ctr = peer_stats.get("avg_ctr", 0)

    trigger_kind = trigger.get("kind", "unknown")

 # -------------------------------
# STEP 3: Trigger-based logic
# -------------------------------

    signals = merchant.get("signals", [])

    if trigger_kind == "perf_dip":

        body = (
            f"{name} ({locality}), aapka CTR {ctr:.2%} hai, "
            f"jabki {city} mein similar businesses ka avg {peer_ctr:.2%} hai. "
        )

        # 🔥 Add signal-based personalization
        if any("stale_posts" in s for s in signals):
            body += " Aapke Google posts kaafi time se update nahi hue."

        # 🔥 Add curiosity hook
        body += " Aap nearby customers miss kar rahe hain. Want me to fix this in 5 min?"

        cta = "YES/STOP"


    elif trigger_kind == "research_digest":

        payload = trigger.get("payload", {})
        item = payload.get("top_item", {})

        title = item.get("title", "a new update")
        source = item.get("source", "")

        body = (
            f"{name}, new research: {title} "
            f"{f'({source})' if source else ''}. "
            f"Yeh aapke patients ke liye useful ho sakta hai. "
            f"Want me to simplify & draft a WhatsApp for you?"
        )

        cta = "YES/STOP"


    else:

        body = (
            f"Hi {name}, ek quick idea hai aapke business grow karne ke liye. "
            f"Want to see?"
        )

        cta = "YES/STOP"

    # -------------------------------
    # STEP 4: Return final output
    # -------------------------------
    return {
        "body": body,
        "cta": cta,
        "send_as": "vera",
        "suppression_key": trigger.get("id", "no_id"),
        "rationale": f"Message generated for {trigger_kind}"
    }