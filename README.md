Instructions to Run:
1. Clone this repo using SSH or HTTP Link
2. Navigate to Project Folder
3. Run player tracking module directly using " python3 run.py player_tracking.py "
4. To run possession and passes module:
   i. install poetry on your device
  ii. run poetry install to install neccessary dependencies
 iii. activate environment using command "poetry shell"
  iv. To run possession module: " python run.py --possession --model models/ball.pt --video videos/soccer_possession.mp4 "
   v. To run passes module: " python run.py --passes --model models/ball.pt --video videos/soccer_passes.mp4 "
5. Model will geenrate output file upon running with results
