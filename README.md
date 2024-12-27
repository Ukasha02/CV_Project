Instructions to Run:
1. Clone this repo using SSH or HTTP Link
2. Navigate to Project Folder
3. Run player tracking module directly using " python3 player_tracking.py "
4. To run possession and passes module:
5. install poetry on your device
6. run poetry install to install neccessary dependencies
7. activate environment using command "poetry shell"
8. To run possession module: " python run.py --possession --model models/ball.pt --video videos/soccer_possession.mp4 "
9. To run passes module: " python run.py --passes --model models/ball.pt --video videos/soccer_passes.mp4 "
10. Model will geenrate output file upon running with results
11. We would adivse you to run this on python 3.9 so that it depedencies don't cause an issue
