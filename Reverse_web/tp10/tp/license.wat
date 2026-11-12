(module
  (type (;0;) (func (result i32)))
  (type (;1;) (func (param i32) (result i32)))
  (import "env" "seed" (func (;0;) (type 0)))
  (func (;1;) (type 0) (result i32)
    i32.const 65568)
  (func (;2;) (type 1) (param i32) (result i32)
    (local i32 i32 i32 i32)
    i32.const 0
    local.set 1
    block  ;; label = @1
      local.get 0
      i32.const 17
      i32.ne
      br_if 0 (;@1;)
      i32.const 0
      local.set 1
      call 0
      local.tee 0
      i32.const 0
      i32.load8_u offset=65568
      i32.xor
      i32.const 255
      i32.and
      i32.const 48
      i32.ne
      br_if 0 (;@1;)
      i32.const 21
      local.set 1
      block  ;; label = @2
        block  ;; label = @3
          loop  ;; label = @4
            local.get 1
            i32.const 37
            i32.eq
            br_if 1 (;@3;)
            local.get 1
            i32.const 65516
            i32.add
            i32.load8_u
            local.get 1
            i32.const 65548
            i32.add
            i32.load8_u
            local.get 1
            i32.const -1
            i32.add
            local.get 0
            i32.xor
            i32.xor
            i32.const 255
            i32.and
            i32.ne
            br_if 1 (;@3;)
            local.get 1
            local.get 0
            i32.xor
            local.set 2
            local.get 1
            i32.const 65549
            i32.add
            local.set 3
            local.get 1
            i32.const 65517
            i32.add
            local.set 4
            local.get 1
            i32.const 2
            i32.add
            local.set 1
            local.get 4
            i32.load8_u
            local.get 2
            local.get 3
            i32.load8_u
            i32.xor
            i32.const 255
            i32.and
            i32.eq
            br_if 0 (;@4;)
          end
          local.get 1
          i32.const -22
          i32.add
          local.set 1
          br 1 (;@2;)
        end
        local.get 1
        i32.const -21
        i32.add
        local.set 1
      end
      local.get 1
      i32.const 15
      i32.gt_u
      local.set 1
    end
    local.get 1)
  (table (;0;) 1 1 funcref)
  (memory (;0;) 2)
  (global (;0;) (mut i32) (i32.const 65536))
  (export "memory" (memory 0))
  (export "buffer" (func 1))
  (export "check" (func 2))
  (data (;0;) (i32.const 65536) "#\10S\0e\15_\5c\1e^5!;6\01c\07\18"))
