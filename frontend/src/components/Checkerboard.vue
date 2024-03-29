<template>
  <div class="checkerboard">
    <CheckerboardBase :baseData="piecesData.baseData" />
    <div style="position: absolute; top: 250px; right: 100px;">
      <table>
        <tr v-for="(row, i) in l" :key="i">
          <td v-for="(col, j) in row" :key="j" style="width: 20px; height: 20px; border: 1px solid #000; text-align: center; font-size: 12px; color: #000; background: #fff;">
            {{ col != 0 ? col.toFixed(2):0 }}
          </td>
        </tr>
      </table>
    </div>
    <p>avg_visits: {{ avg_visits.toFixed(2) }}, pre_visits: {{ pre_visits.toFixed(2) }}, rate: {{ rate.toFixed(2) }}</p>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import { pieceColor, piecesData, opponent, priority } from '../constant'
import { forEach, pick } from '../tools'
import CheckerboardBase from './CheckerboardBase.vue'

export default {
  name: 'checkerboard',
  components: {
    CheckerboardBase
  },
  data () {
    return {
      // 棋子数据
      piecesData: {},
      // 优先排序
      priority: {},
      // 自动下一棋时间（毫秒）
      automaticMsec: 100,
      // 对手是不是电脑
      isComputer: false,
      avg_visits: 0,
      pre_visits: 0,
      rate: 0,
      l: []
    }
  },
  computed: mapState({
    fall: state => state.fall,
    user: state => state.user,
    opponent: state => state.opponent,
    downPiece: state => state.downPiece,
    roundNum: state => state.roundNum,
    countDown: state => state.countDown,
    mode: state => state.mode,
    automatic: state => state.automatic,
    logPieces: state => state.logPieces
  }),
  watch: {
    roundNum () {
      this.initData()
    },
    downPiece (val) {
      this.handlePiece(val)
    },
    automatic (val) {
      val && (this.logPieces.length === 0 ? this.setDownPiece(this.piecesData.baseData['8-8']) : this.computerDownPiece())
    }
  },
  created () {
    window.cb = this

    this.isComputer = this.mode.value === opponent.simpleComputer.value // || this.mode.value === opponent.difficultComputer.value

    // 无计时，直接开始
    !this.countDown && this.start()
  },
  methods: {
    ...mapActions(['victory', 'start', 'draw']),
    ...mapMutations(['setFall', 'setDownPiece']),
    // 下棋子处理
    handlePiece (data) {
      let item = this.piecesData.baseData[data.key]
      item.value = this.fall

      // 下棋子后是不是结束
      if (this.handleIsOver(item) === true) {
        this.victory()
        return
      }

      // 未结束，设置轮换
      if (this.fall === pieceColor.black.value) {
        // 当前下黑子
        // 棋子设为黑色
        item.text = pieceColor.black.text
        // 切换到白色下
        this.setFall(pieceColor.white.value)
      } else {
        item.text = pieceColor.white.text
        this.setFall(pieceColor.black.value)
      }

      // 电脑
      if (this.isComputer) {
        // 处理棋子优先级
        this.handlePriority(item)

        if (this.automatic) {
          setTimeout(this.computerDownPiece, this.automaticMsec)
        } else if (this.fall === this.opponent.color.value)  {
          // 轮到电脑自动下
          this.computerDownPiece()
        }
      } else {
        // MCTS 下棋
        // console.log(data)
        // console.log(this.piecesData)
        if(data.text == '黑') {
          console.log('用户下的', data.x, data.y)
          // 随机决策
          // while(data.x) {
          //   let x = ~~Math.floor(Math.random() * 10) + 1
          //   let y = ~~Math.floor(Math.random() * 10) + 1
          //   if(!this.piecesData?.baseData[`${ x }-${ y }`]?.value) {
          //     console.log('AI随机决策', x, y)
          //     this.setDownPiece(this.piecesData.baseData[`${ x }-${ y }`]);
          //     break;
          //   }
          // }
          
          // make CheckerboardBase style disable (class=checkerboard)
          let pe = document.querySelector('.checkerboard').style.pointerEvents
          document.querySelector('.checkerboard').style.pointerEvents = 'none'
          
          fetch(`http://${window.location.host.split(':')[0]}:8001/hello?x=${data.x}&y=${data.y}`).then(res => res.json()).then(res => {
            console.log('AI决策', res.x, res.y)
            this.setDownPiece(this.piecesData.baseData[`${ res.x }-${ res.y }`]);
            this.avg_visits = res.avg_visits
            this.pre_visits = res.pre_visits
            this.rate = res.rate
            this.l = res.l
            // make CheckerboardBase style enable (class=checkerboard)
            document.querySelector('.checkerboard').style.pointerEvents = pe
          })
        }
        
      }
    },
    handlePriority (data) {
      // 获取该棋子所在排的棋子值
      forEach(this.priority.pieceBaseKey[data.key], (kss, direction) => {
        forEach(kss, (keys, index) => {
          // 当前值
          let newValues = []
          // 当前棋子值为空子值
          let oldValues = []
          forEach(keys, (key) => {
            let val = this.piecesData.baseData[key].value
            newValues.push(val)
            if (key === data.key) {
              oldValues.push(pieceColor.none.value)
            } else {
              oldValues.push(val)
            }
          })
          // 更新排数据
          this.priority.updateItem(data.key, direction, index, newValues, oldValues)
        })
      })
    },
    computerDownPiece () {
      // 获取优先棋子
      let keys = this.priority.getBestKeys(this.fall)
      if (keys.length === 0) {
        // 和局
        this.draw()
      } else {
        // 当多个时随机
        this.setDownPiece(this.piecesData.baseData[keys[Math.floor(Math.random() * keys.length)]])
      }
    },
    // 检查是否是五子相连
    handleIsOver (data) {
      let isOver = false
      let item = this.piecesData.countData[data.key]

      let tItems = this.getConnections(item.tk)
      let bItems = this.getConnections(item.bk)

      let rtItems = this.getConnections(item.rtk)
      let lbItems = this.getConnections(item.lbk)

      let rItems = this.getConnections(item.rk)
      let lItems = this.getConnections(item.lk)

      let rbItems = this.getConnections(item.rbk)
      let ltItems = this.getConnections(item.ltk)

      let connections = [data]

      if (1 + tItems.length + bItems.length > 4) {
        connections = connections.concat(tItems, bItems)
        isOver = true
      }
      if (1 + rtItems.length + lbItems.length > 4) {
        connections = connections.concat(rtItems, lbItems)
        isOver = true
      }
      if (1 + rItems.length + lItems.length > 4) {
        connections = connections.concat(rItems, lItems)
        isOver = true
      }
      if (1 + rbItems.length + ltItems.length > 4) {
        connections = connections.concat(rbItems, ltItems)
        isOver = true
      }

      if (isOver) {
        for (let i in connections) {
          connections[i].active = true
        }
      }

      return isOver
    },
    // 获取相连棋子
    getConnections (itemKeys) {
      let connections = []
      for (let i in itemKeys) {
        let item = this.piecesData.baseData[itemKeys[i]]
        if (item.value === this.fall) {
          connections.push(item)
        } else {
          break
        }
      }
      return connections
    },
    // 初始化
    initData () {
      // 黑子先手
      this.setFall(pieceColor.black.value)

      this.piecesData = new piecesData()

      // 电脑
      if (this.isComputer) {
        this.priority = new priority()
        this.priority.setPieceBaseKeys(pick(this.piecesData, ['tbk', 'lrk', 'ltrbk', 'rtlbk']))
        if (this.fall === this.opponent.color.value || this.automatic) {
          this.setDownPiece(this.piecesData.baseData['8-8'])
        }
      }
      fetch(`http://${window.location.host.split(':')[0]}:8001/create`).then(res => res.json()).then(res => {
        console.log(res)
      })
    }
  }
}
</script>
