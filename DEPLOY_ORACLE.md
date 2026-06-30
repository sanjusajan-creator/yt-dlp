# Deploy yt-dlp Backend to Oracle Cloud Free Tier (Always-Free)

## Step 1: Create Oracle Cloud Account

1. Go to https://cloud.oracle.com/free
2. Sign up for **Always Free** account (credit card required for verification, not charged)
3. Select **Region**: Choose closest to you (e.g., `ap-mumbai-1`, `us-ashburn-1`)

## Step 2: Create ARM VM Instance

1. Dashboard → **Create a VM** → **Create compute instance**
2. **Name**: `ytdlp-backend`
3. **Image**: `Ubuntu 22.04` (or Oracle Linux 8)
4. **Shape**: `VM.Standard.A1.Flex` (ARM, always-free)
   - **OCPU**: 4
   - **Memory**: 24 GB
5. **Public SSH key**: Paste your SSH public key (generate with `ssh-keygen` on your PC)
6. **Add block storage**: 50 GB (free)
7. **Create** → Note the **Public IP**

## Step 3: Open Port 8000

1. Go to **Networking** → **Virtual Cloud Networks** → your VCN
2. **Security Lists** → **Default Security List**
3. **Add Ingress Rules**:
   - Source CIDR: `0.0.0.0/0`
   - Destination Port: `8000`
   - Description: `yt-dlp API`

## Step 4: SSH and Deploy

```bash
# SSH into your VM
ssh -i ~/.ssh/your_key ubuntu@YOUR_VM_IP

# Run the deployment script
curl -s https://raw.githubusercontent.com/sanjusajan-creator/yt-dlp/main/deploy-oracle.sh | bash
# Or clone and run manually:
# git clone https://github.com/sanjusajan-creator/yt-dlp.git /opt/ytdlp-backend
# cd /opt/ytdlp-backend
# chmod +x deploy-oracle.sh
# ./deploy-oracle.sh
```

When prompted, paste your `YT_COOKIES_B64` value.

## Step 5: Test

```bash
# From your VM:
curl http://localhost:8000/debug/cookies
curl http://localhost:8000/audio?video_id=dQw4w9WgXcQ

# From your PC:
curl http://YOUR_VM_IP:8000/audio?video_id=dQw4w9WgXcQ
curl http://YOUR_VM_IP:8000/audio/stream?video_id=dQw4w9WgXcQ
```

## Step 6: Update Mobile App

Once confirmed working, update `mobile/vibecraft-mobile/lib/api.ts`:

```typescript
const SELF_HOSTED_API_BASE = 'http://YOUR_VM_IP:8000';
```

**Note**: For production, add a domain + HTTPS with nginx + Let's Encrypt.
For now, Android requires `android:usesCleartextTraffic="true"` in AndroidManifest.xml for HTTP.

## Firewall Rules (if needed)

```bash
sudo ufw allow 8000/tcp
sudo ufw enable
```

## Auto-restart on reboot

Docker `restart: unless-stopped` handles this automatically.
