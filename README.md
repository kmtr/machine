# Machine Controller

Machineを制御するためのソフトウェアです。
OSC Serverを内蔵し、外部からのOSCメッセージによって制御を行います。

# Setup

以下のライブラリに依存します。

- python-osc
- pigpio

このうちpigpioはRaspbbery Pi上のLinuxでのみ動作します。
いずれのプラットフォームでも以下のコマンドで必要なライブラリがインストールされます。

```sh
python install.py
```

# 起動

## 起動時引数

### --ip

OSC ServerとしてListenするIPを指定します。指定しない場合は127.0.0.1が使われます。

### --port

OSC ServerとしてListenするportを指定します。指定しない場合は5005が使われます。

### --gui

Trueを指定すると、GUIモードとなります。
GUIモードではGPIOに信号は送られません。

### --debug

Trueを指定すると詳細なログが出力されます。


## 例

### 通常モード

- IP指定
- PORT指定
- debugあり

```
python main.py --ip 0.0.0.0 --port 5015 --debug True
```

### GUIモード

```
python main.py --gui True
```

## OSCメッセージ

Machineが受け付けるOSCメッセージは、`osc_server.py`で定義されています。

### /ping

OSC Serverのコンソールに`pong`と出力されます。

### /reset

全ての腕をリセットします。

### /pattern pattern_number:int

パターン番号を指定し、腕の状態を決定します。
パターンは`patterns.py`で定義されています。

例
```
/pattern 1
```

### /set key:int angle:int

keyで指定した脚についた腕を`angle`度回転させます。
keyはGPIOの番号ではありません。keyとGPIOの対応関係は、`Machine.KEY_GPIO_MAP`で定義されています。
脚にはそれぞれ向きがあり、回転方向はその向きに依存します。
GUIモードにおける足の向きは`pigpio_gui.py`の`buildLegs`で定義されています。

例
```
/set 1 90
```

## 注意

モーターを保護するため、腕はおおよそ0~180度の範囲でしか動きません。