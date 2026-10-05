# AWS pe deploy (EC2 + Docker Compose, sabse sasta aur simple)

**Instance:** t3.small (2 GB RAM) Ubuntu 24.04, 20 GB gp3 disk. ~$15/month. (t3.micro mein RAM kam padegi.)

## 1. EC2 banao (AWS Console)
- Security Group inbound: SSH (22) **sirf My IP**, Custom TCP 8501 (UI), 8000 (API). 5433 kabhi open mat karna.
- Key pair download karo (`aipos.pem`).

## 2. Laptop se server mein jao
```bash
chmod 400 ~/Downloads/aipos.pem
ssh -i ~/Downloads/aipos.pem ubuntu@<EC2-PUBLIC-IP>
```

## 3. Server pe Docker install
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu && exit     # logout, phir dobara ssh karo
```

## 4. Code bhejo (laptop se, project folder ke bahar se)
```bash
rsync -av --exclude .env --exclude .venv -e "ssh -i ~/Downloads/aipos.pem" aipos/ ubuntu@<EC2-PUBLIC-IP>:~/aipos/
```
(Ya GitHub pe push karke server pe `git clone`.)

## 5. Server pe .env banao aur chalao
```bash
cd ~/aipos && cp .env.example .env && nano .env
# OPENAI_API_KEY, strong POSTGRES_PASSWORD, aur APP_API_KEY (random string) set karo
docker compose up -d --build
docker compose ps        # sab "healthy" hone chahiye
```
UI: `http://<EC2-PUBLIC-IP>:8501`  |  API docs: `http://<EC2-PUBLIC-IP>:8000/docs`

APP_API_KEY set kiya hai to API calls mein `X-API-Key: <key>` header lagao. (Streamlit UI .env se khud le leta hai.)

## 6. Update karna
```bash
git pull && docker compose up -d --build
```

## Security & cost tips
- HTTPS chahiye to Caddy/Nginx + domain lagao (baad ka step).
- AWS Budgets mein $20 ka alert laga do.
- Server ke saath-saath **OpenAI usage limit** bhi set karo, public API pe bills badh sakte hain.
- Backup: `docker compose exec postgres pg_dump -U aipos aipos > backup.sql`
