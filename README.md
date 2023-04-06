Игра змейка

Запуск приложения осуществляется через запуск файла main.py.
При запуске появится основное меню приложения. Будет четыре кнопки: Start, Settings, Table of Records, Quit game

Игровой процесс
Нажатие на кнопку Start запускает игровой процесс, скрывается меню и открывается окно с игрой в змейку и генерируется рандомный уровень с произвольной начальной расстановкой стенок и произвольно разбросанным количеством еды, которое не превышает некоторого значения в зависимости от уровня сложности(об этом позже). Управление змейкой осуществяется через стрелки на клавиатуре. Также можно завершить игру нажав клавишу esc. Черные зоны на игровом поле это стены, при врезании змейку в одну из них игра завершается. Когда змейка врезается в себя, игра также завершается. На игровом поле периодически появляются разноцветные квадратики, это еда, когда змейка пересекается с одним из таких квадратиков, то рандомно с разной вероятностью происходит один из следующих эффектов: змейка увеличивается на один базовый блок, змейка уменьшается на один блок, скорость змейки увеличивается, скорость змейки уменьшается, окраска змейки меняется на радужную(или наоборот окраска отключается), форма змейки меняется на более красивую(появляется хвостик и шершавости при поворотах, или наоборот форма змейки меняется на стандартную). В случае, если длина змейки минимальная или скорость достигла минимального или максимального значения, может ничего не произойти.

Завершение игры
Когда игра завершилась, появится окошко, куда пользователь может ввести свое имя для сохранения в таблице рекордов. Если пользователь уже был в таблице рекордов и он записал свое имя, то в таблице рекордов будет сохранен его наилучший результат. Максимальная длина имени 16 символов. Имя может содеражать любые символы, пустого имени не существует(то есть если пользователь введет пустое имя, то его результат не сохранится). Для сохранения имени нужно нажать на кнопку «Enter your name». Если пользователь не хочет сохранять свой рекорд, то ему следует нажать на кнопку «Close». 

Некоторые параметры игры:
Частота обновления экрана 60 кадров в секунду
Размер базового блока равен 20x20 пикселей
При нажатии на кнопку Settings  в меню пользователю открывается окно настроек. Там он может выбрать уровень сложности и цвет змейки. Есть три уровня сложности
Easy:
1. Начальная скорость змейки равна 1 пикселю в кадр
2. Максимальная скорость змейки ограничена 6 пикселями в кадр
3. Максимальное количество стенок на уровне не превышает 7
4. Максимальная длина стенки не превышает 15 базовых блоков
5. Количество кадров между соседними увеличениями скорости змейки равно хотя бы 360(еда может увеличивать скорость вне зависимости от этого времени)
6. При увеличении скорости змейки увеличение ее скорости будет случаться намного реже
7. Максимальное начальное количество еды на уровне не превышает 20
Medium:
1. Начальная скорость змейки равна 2 пикселям в кадр
2. Максимальная скорость змейки ограничена 9 пикселями в кадр
3. Максимальное количество стенок на уровне не превышает 10
4. Максимальная длина стенки не превышает 20 базовых блоков
5. Количество кадров между соседними увеличениями скорости змейки равно хотя бы 300(еда может увеличивать скорость вне зависимости от этого времени)
6. При увеличении скорости змейки увеличение ее скорости будет случаться реже
7. Максимальное начальное количество еды на уровне не превышает 10
Hard:
1. Начальная скорость змейки равна 4 пикселям в кадр
2. Максимальная скорость змейки ограничена 12 пикселями в кадр
3. Максимальное количество стенок на уровне не превышает 20
4. Максимальная длина стенки не превышает 30 базовых блоков
5. Количество кадров между соседними увеличениями скорости змейки равно 300(еда может увеличивать скорость вне зависимости от этого времени)
6. Максимальное начальное количество еды на уровне не превышает 10
Уровень сложности по дефолту стоит Medium

Score:
Количество набранных игроком очков соответствует длине его змейки, изначальная длина змейки равна 0, при поеданию еды длина может увеличиваться на один базовый блок или уменьшаться на один базовый блок, количество базовых блоков в змейке и определяет счет(score)

Table of records:
При нажатии кнопки Table of Records в меню открывается таблица рекордов.
В ней есть три столбца: в первом столбце указано место игрока, во втором его имя, в третьем максимальное количество набранных игроком очков. Если пользователь хочет удалить имя какого-то игрока из таблица рекордов, то он должен нажать на соответствующую строку и нажать кнопку «Delete row». После этого высветится окно с подтверждением того, что пользователь хочет удалить данную строку таблицы. После удаления, чтобы таблица обновилась, нужно выйти в основное меню и перезайти в таблицу. Пользователь может покинуть таблицу рекордов, нажав на кнопку «Close». В таблице может храниться произвольное количество пользователей, поэтому имеется возможность скроллинга таблицы лидеров, которая может понадобиться, если пользователей слишком много.

Quit game
Нажатие на кнопку «Quit game»  в основном меню завершает работу программы.
