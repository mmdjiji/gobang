<template>
  <div class="content">
    <div class="checkerboard" style="width: 400px; height: 400px;">
      <div class="line-row"></div>
      <div class="line-col"></div>
      <div class="spot"></div>
      <div class="num">
        <div v-for="n in 10" :key="n">{{ n }}</div>
      </div>
      <div class="letter">
        <div v-for="n in 10" :key="n">{{ n - 1 | letter }}</div>
      </div>
      <div class="pieces">
        <div class="row" v-for="y in 10" :key="y">
          <Piece v-for="x in 10" :key="x" :data="baseData[`${ x }-${ y }`]" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Piece from './Piece.vue'

export default {
  name: 'checkerboard',
  props: {
    baseData: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  components: {
    Piece
  }
}
</script>

<style lang="stylus" scoped>
.content {
  padding: 20px;
  width: 440px;
  height: 440px;
}

.checkerboard {
  position: relative;
  flex-shrink: 0;
  width: 400px;
  height: 400px;
  background-color: #E7C29C;
  font-size: 12px;
  box-shadow: 3px 3px 12px;
}

// 横线
.line-row{
  position: absolute;
  top: 0;
  left: 0;
  width: 361px;
  height: 1px;
  box-shadow: 20px 20px, 20px 60px, 20px 100px, 20px 140px, 20px 180px, 20px 220px, 20px 260px, 20px 300px, 20px 340px, 20px 380px; //, 20px 420px, 20px 460px, 20px 500px, 20px 540px, 20px 580px;
}

// 列线
.line-col{
  position: absolute;
  top: 0;
  left: 0;
  width: 1px;
  height: 361px;
  box-shadow: 20px 20px, 60px 20px, 100px 20px, 140px 20px, 180px 20px, 220px 20px, 260px 20px, 300px 20px, 340px 20px, 380px 20px; //, 420px 20px, 460px 20px, 500px 20px, 540px 20px, 580px 20px;
}

// 5个点
.spot {
  position: absolute;
  display: none;
  top: 37px;
  left: 37px;
  width: 7px;
  height: 7px;
  background-color: black;
  box-shadow: 320px 0, 160px 160px, 320px 320px, 0 320px;
}

// 左边数字
.num {
  position: absolute;
  top: 0;
  left: -20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  width: 20px;
  height: 100%;
}

// 上边字母
.letter {
  position: absolute;
  top: -20px;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 100%;
  height: 20px;
}

// 全部棋子
.pieces {
  position: absolute;
  top: 0;
  left: 0;

  .row {
    display: flex;
  }
}

</style>

