python -m venv venv
echo "source dev.sh" >> venv/**/activate
if ! test -f .env; then
    cp .env.template .env
fi
source venv/**/activate
cd backend
pip install -r requirements.txt
cd ../frontend
npm install