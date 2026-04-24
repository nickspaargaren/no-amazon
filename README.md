[![no-amazon](https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/GAFAMSPLATTEXTgit.png)](https://github.com/nickspaargaren/no-amazon)

# Block All Amazon Services on Your Network

This blocklist prevents all devices on your home network from accessing Amazon websites and services. Use this if you want to completely remove Amazon from your digital life for privacy or personal reasons.

> **⚠️ IMPORTANT**: This blocks **ALL** Amazon services. Read the "What Will Stop Working" section below before using this list.

---

## What Will Stop Working

When you use this blocklist, the following services and websites will **completely stop working**:

### Amazon Services You Can't Use:

- **Amazon.com** - No online shopping on Amazon
- **Prime Video** - Cannot stream movies or TV shows
- **Twitch** - Streaming platform will not work
- **IMDb** - Movie database website will be blocked
- **Audible** - Audiobook service will not work
- **Amazon Music** - Music streaming will be blocked
- **Kindle Cloud Reader** - Cannot read books online
- **Whole Foods online ordering** - Website will not load
- **Ring** - Smart doorbell services may be affected
- **Alexa web services** - Voice assistant cloud features

### Other Websites That May Break:

- **Many websites use Amazon's servers (AWS)** - Some websites you visit regularly might stop working because they're hosted on Amazon's cloud infrastructure
- **Apps and services** - Mobile apps and services that rely on Amazon's backend may fail

### Devices That May Have Issues:

- **Fire TV Stick** - Will crash on startup (see workaround below)
- **Kindle e-readers** - Cannot download new books or sync
- **Echo devices** - Smart speakers will lose most functionality
- **Ring doorbells/cameras** - May lose cloud features

---

## Why Would I Use This?

This blocklist is for people who want to:

- **Protect their privacy** - Reduce data collection by Amazon
- **Avoid monopolies** - Stop supporting large tech companies
- **Digital minimalism** - Remove convenient but unnecessary services
- **Take a stand** - Make a personal choice about which companies to support

**This is a significant lifestyle change.** You're choosing privacy and principles over convenience. Make sure you're ready for the trade-offs.

---

## How to Use This Blocklist

You'll need a network-level ad blocker to use this list. Here are the most common options:

### Option 1: Pi-hole

**What is Pi-hole?** A device (usually a Raspberry Pi) that blocks ads and trackers for your entire home network.

1. Log in to your Pi-hole admin interface (usually at `http://pi.hole/admin`)
2. Click on **Group Management** → **Adlists**
3. Paste this URL in the "Address" field:
   ```
   https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/parsedamazon
   ```
4. Click **Add**
5. Go to **Tools** → **Update Gravity** to apply the changes

### Option 2: AdGuard Home

**What is AdGuard Home?** Similar to Pi-hole, blocks ads and trackers on your network.

1. Open your AdGuard Home admin interface
2. Go to **Filters** → **DNS blocklists**
3. Click **Add blocklist** → **Add a custom list**
4. Paste this URL:
   ```
   https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/amazon-adguard.txt
   ```
5. Click **Save**

### Option 3: Unbound DNS Server

**What is Unbound?** An advanced DNS server for tech-savvy users.

1. Download the configuration file:
   ```bash
   sudo curl -o /etc/unbound/unbound.conf.d/amazon-blocklist.conf \
     https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/amazon-unbound.conf
   ```
2. Restart Unbound:
   ```bash
   sudo systemctl restart unbound
   ```

---

## Block Only Specific Amazon Services (Advanced)

If blocking everything is too extreme, you can block specific categories instead:

| Category         | What It Blocks                      | Use This If You Want To...             |
| ---------------- | ----------------------------------- | -------------------------------------- |
| **General**      | Core Amazon domains (shopping, AWS) | Block shopping but keep other services |
| **CloudFront**   | Amazon's CDN (content delivery)     | Block Amazon's infrastructure          |
| **Twitch**       | Twitch streaming platform only      | Block Twitch but keep Prime Video      |
| **IMDb**         | IMDb movie database only            | Block IMDb but keep other services     |
| **Amazon Video** | Prime Video streaming only          | Block streaming but keep shopping      |

**Category list URLs:**

- General: `https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/categories/generalparsed`
- CloudFront: `https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/categories/cloudfrontparsed`
- Twitch: `https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/categories/twitchparsed`
- IMDb: `https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/categories/imdbparsed`
- Amazon Video: `https://raw.githubusercontent.com/nickspaargaren/no-amazon/master/categories/amazonvideoparsed`

Add these URLs to your Pi-hole or AdGuard the same way as the main list.

---

## Frequently Asked Questions

### Will this break my internet?

No, your internet will work fine. Only Amazon services and websites hosted on Amazon's servers will be blocked. Most of the internet will work normally.

### Can I still use my Fire TV Stick?

Yes, but you need to unblock two specific domains:

- `fireoscaptiveportal.com`
- `firetvcaptiveportal.com`

Without these, your Fire TV will crash on the home screen. To unblock them, add them to your Pi-hole or AdGuard whitelist. This allows the Fire TV to boot while still blocking other Amazon services.

### What if a website I need stops working?

Some websites are hosted on Amazon's servers (AWS). If a site you need stops working:

1. **Temporarily disable the blocklist** to confirm it's the cause
2. **Whitelist that specific domain** in your Pi-hole/AdGuard settings
3. **Use category lists instead** of the full blocklist to be more selective

### How do I unblock everything if I change my mind?

In Pi-hole: Go to **Group Management** → **Adlists**, find the Amazon list, and click the red trash icon to remove it. Then update Gravity.

In AdGuard: Go to **Filters** → **DNS blocklists**, find the Amazon list, and click the trash icon.

### Can I use this on my phone only?

This blocklist works at the network level, so it affects all devices on your home WiFi. For phone-only blocking, you'd need a VPN-based ad blocker app like Blokada or AdGuard for mobile (different from AdGuard Home).

### Will Amazon know I'm blocking them?

No. From Amazon's perspective, it just looks like you're not visiting their websites. There's no way for them to detect this.

---

## Contributing

Want to add more Amazon domains to the list? Contributions are welcome!

1. Fork this repository
2. Add domains to `amazon.txt` under the appropriate category
3. Submit a pull request

Please ensure domains are valid and actually belong to Amazon.

---

## Technical Information

### What is GAFAM?

GAFAM stands for **Google, Amazon, Facebook, Apple, and Microsoft** - the five largest tech companies. These companies are influential in the digital economy and are often criticized for:

- Collecting massive amounts of user data
- Monopolistic business practices
- Tax avoidance
- Political influence

This project is part of a broader effort to reduce dependence on these tech giants.

### For Developers

**Setup**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Testing the blocklist**

```bash
pytest tests/
```

**Type checking**

```bash
mypy
```

Type checking runs automatically in CI on all pull requests.

**Code formatting:**

Check formatting
```bash
black --check .
```

Fix formatting
```bash
black .
```

Code formatting is checked automatically in CI on all pull requests.

**Generating blocklist formats**

```bash
python3 convert.py --help       # Show all available commands
python3 convert.py all          # Generate all formats
python3 convert.py pihole       # Pi-hole format only
python3 convert.py adguard      # AdGuard format only
python3 convert.py unbound      # Unbound format only
python3 convert.py categories   # Category-specific lists
python3 convert.py json         # Output data in JSON format
```

For detailed help on any command:
```bash
python3 convert.py <command> --help
```

---

## License

This project is open source. Use it freely to protect your privacy and reduce your dependence on Amazon.
