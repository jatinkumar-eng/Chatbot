def compose(category, merchant, trigger, customer=None):

    # -------------------------------
    # STEP 1: Customer message
    # -------------------------------
    if customer is not None:
        cust_name = customer.get("identity", {}).get("name", "Customer")
        merchant_name = merchant.get("identity", {}).get("name", "your clinic")

        body = (
            f"Hi {cust_name}, {merchant_name} here 🦷 "
            f"5–6 months ho gaye last visit ko — cleaning due hai. "
            f"Is week slot book karna hai?"
        )

        return {
            "body": body,
            "cta": "open_ended",
            "send_as": "merchant_on_behalf",
            "suppression_key": trigger.get("id", "no_id"),
            "rationale": "Customer recall reminder"
        }

    # -------------------------------
    # STEP 2: Safe data extraction
    # -------------------------------
    identity = merchant.get("identity", {})
    performance = merchant.get("performance", {})
    peer_stats = category.get("peer_stats", {})

    name = identity.get("name", "Merchant")
    locality = identity.get("locality", "")
    city = identity.get("city", "")

    ctr = float(performance.get("ctr", 0) or 0)
    peer_ctr = float(peer_stats.get("avg_ctr", 0) or 0)

    trigger_kind = trigger.get("kind", "unknown")
    signals = merchant.get("signals", [])

    # -------------------------------
    # STEP 3: Trigger-based logic
    # -------------------------------

    if trigger_kind == "perf_dip":

        body = (
            f"{name} ({locality}) — aapka CTR {ctr:.2%} hai, "
            f"jabki {city} ka avg {peer_ctr:.2%} hai. "
        )

        # Add signal-based personalization
        if any("stale_posts" in s for s in signals):
            body += "Last post kaafi purana hai — customers fresh content nahi dekh pa rahe. "

        # Add compulsion (loss + curiosity)
        body += (
            "Is wajah se nearby searches miss ho rahe hain. "
            "Main 5 min mein exact fix dikha doon?"
        )

        cta = "YES/STOP"

    elif trigger_kind == "research_digest":

        payload = trigger.get("payload", {})
        item = payload.get("top_item", {})

        title = item.get("title", "new update")
        source = item.get("source", "")

        body = (
            f"{name}, aaj ka research update: {title} "
            f"{f'({source})' if source else ''}. "
            f"Yeh aapke patients ke liye useful ho sakta hai. "
            f"Chahen to main iska simple WhatsApp draft bana doon?"
        )

        cta = "YES/STOP"

    else:

        body = (
            f"{name}, ek quick growth idea hai aapke business ke liye "
            f"{locality} area mein. Want to see?"
        )

        cta = "YES/STOP"

    # -------------------------------
    # STEP 4: Final output
    # -------------------------------
    return {
        "body": body,
        "cta": cta,
        "send_as": "vera",
        "suppression_key": trigger.get("id", "no_id"),
        "rationale": f"Message generated for {trigger_kind}"
    }
