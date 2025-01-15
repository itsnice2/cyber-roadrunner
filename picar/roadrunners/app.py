from flask import Flask, request
import picar_4wd as fc


app = Flask(__name__)

@app.route('/control', methods=['POST'])
def control():
    command = request.form.get('command')
    if command == 'forward':
        fc.left_front.set_power( 100 ) 
        fc.right_front.set_power( 100 )
        fc.left_rear.set_power( 100 )                    
        fc.right_rear.set_power( 100 )
        pass
    elif command == 'backward':
        fc.left_front.set_power( -100 ) 
        fc.right_front.set_power( -100 )
        fc.left_rear.set_power( -100 )                    
        fc.right_rear.set_power( -100 )
        pass
    elif command == 'left':
        fc.left_front.set_power( -50 )
        fc.right_front.set_power( 50 )
        fc.left_rear.set_power( -50 )                     
        fc.right_rear.set_power( 50) 
        pass
    elif command == 'right':
        fc.left_front.set_power( 50 )
        fc.right_front.set_power( -50 )
        fc.left_rear.set_power( 50 )                     
        fc.right_rear.set_power( -50) 
        pass
    elif command == 'stop':
        fc.stop()

    print(command)
    return 'OK'

if __name__ == '__main__':
    app.run(host='10.0.0.25', port=5000)
#    app.run(host='192.168.5.111', port=5000)
